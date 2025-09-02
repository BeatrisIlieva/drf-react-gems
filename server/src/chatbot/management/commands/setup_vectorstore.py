import os
import re
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from decouple import config
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone
from pinecone import Pinecone as PineconeClient


class Command(BaseCommand):
    help = 'Initialize and populate Pinecone vector store with PDF documents'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pdf-file',
            type=str,
            default='product_data.pdf',
            help='Name of the PDF file to process (default: product_data.pdf)'
        )
        parser.add_argument(
            '--index-name',
            type=str,
            help='Pinecone index name (overrides environment variable)'
        )
        parser.add_argument(
            '--force-recreate',
            action='store_true',
            help='Delete existing vectors and recreate the vector store'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually doing it'
        )

    def handle(self, *args, **options):
        try:
            self.stdout.write("Starting vector store setup...")

            # Get configuration
            pdf_file = options['pdf_file']
            index_name = options['index_name'] or os.getenv("PINECONE_INDEX_NAME") or config(
                "PINECONE_INDEX_NAME", default="drf-react-gems-index")
            force_recreate = options['force_recreate']
            dry_run = options['dry_run']

            if dry_run:
                self.stdout.write(
                    self.style.WARNING(
                        "DRY RUN MODE - No changes will be made")
                )

            # Validate environment variables
            self._validate_environment()

            # Initialize embedding model
            embedding_model = OpenAIEmbeddings(
                model="text-embedding-3-small", dimensions=512)
            self.stdout.write("✓ Initialized embedding model")

            # Process PDF
            self.stdout.write(f"Processing PDF: {pdf_file}")
            pages = self._create_pages_from_pdf(pdf_file)
            chunks = self._create_chunks_using_regex(pages)

            self.stdout.write(f"✓ Created {len(chunks)} document chunks")

            if dry_run:
                self.stdout.write(
                    "Would create/update Pinecone vector store with:")
                for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
                    preview = chunk.page_content[:100] + "..." if len(
                        chunk.page_content) > 100 else chunk.page_content
                    self.stdout.write(f"  Chunk {i+1}: {preview}")
                if len(chunks) > 3:
                    self.stdout.write(
                        f"  ... and {len(chunks) - 3} more chunks")
                return

            # Create/update vector store
            vectorstore = self._create_vector_store(
                chunks, embedding_model, index_name, force_recreate)

            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Successfully set up vector store with {len(chunks)} documents")
            )

        except Exception as e:
            raise CommandError(f"Failed to setup vector store: {str(e)}")

    def _validate_environment(self):
        """Validate required environment variables"""
        try:
            pinecone_key = os.getenv('PINECONE_API_KEY') or config(
                'PINECONE_API_KEY', default=None)
            openai_key = os.getenv('OPENAI_API_KEY') or config(
                'OPENAI_API_KEY', default=None)

            print(f"Pinecone API Key: {pinecone_key[:5]}...")
            print(f"OpenAI API Key: {openai_key[:5]}...")

            missing_vars = []
            if not pinecone_key:
                missing_vars.append('PINECONE_API_KEY')
            if not openai_key:
                missing_vars.append('OPENAI_API_KEY')

            if missing_vars:
                raise CommandError(
                    f"Missing required environment variables: {', '.join(missing_vars)}\n"
                    f"Make sure they are set in your .env file or environment."
                )

            self.stdout.write("✓ Environment variables validated")

        except Exception as e:
            if "PINECONE_API_KEY" in str(e) or "OPENAI_API_KEY" in str(e):
                raise CommandError(
                    f"Error loading environment variables: {str(e)}\n"
                    f"Make sure PINECONE_API_KEY and OPENAI_API_KEY are set in your .env file."
                )
            raise

    def _create_pages_from_pdf(self, document_name):
        """Load pages from PDF file"""
        possible_paths = [
            os.path.join(settings.BASE_DIR, "docs", document_name),
            os.path.join(settings.BASE_DIR, document_name),
            os.path.join(os.path.dirname(
                os.path.abspath(__file__)), "docs", document_name),
            document_name  # Absolute path or current directory
        ]

        pdf_path = None
        for path in possible_paths:
            if os.path.exists(path):
                pdf_path = path
                break

        if not pdf_path:
            raise CommandError(
                f"PDF file '{document_name}' not found in any of these locations:\n" +
                "\n".join(f"  - {path}" for path in possible_paths)
            )

        self.stdout.write(f"✓ Found PDF at: {pdf_path}")

        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        if not pages:
            raise CommandError(f"No pages found in PDF: {pdf_path}")

        self.stdout.write(f"✓ Loaded {len(pages)} pages from PDF")
        return pages

    def _create_chunks_using_regex(self, pages):
        """Create document chunks using regex pattern"""
        full_text = "\n".join([p.page_content for p in pages])

        # Extract product blocks using regex
        product_blocks = re.findall(
            r"Collection:.*?stars;", full_text, re.DOTALL
        )

        if not product_blocks:
            self.stdout.write(
                self.style.WARNING(
                    "No product blocks found with the current regex pattern")
            )
            # Fallback: create chunks from pages directly
            chunks = [Document(page_content=page.page_content)
                      for page in pages]
            self.stdout.write(
                f"✓ Created {len(chunks)} chunks from pages directly")
        else:
            chunks = [Document(page_content=block) for block in product_blocks]
            self.stdout.write(
                f"✓ Created {len(chunks)} product chunks using regex")

        return chunks

    def _create_vector_store(self, chunks, embedding_model, index_name, force_recreate=False):
        """Create or update Pinecone vector store"""
        # Initialize Pinecone client
        pc = PineconeClient(api_key=os.getenv(
            "PINECONE_API_KEY") or config("PINECONE_API_KEY"))

        # Check if index exists
        existing_indexes = pc.list_indexes().names()

        if index_name not in existing_indexes:
            raise CommandError(
                f"Index '{index_name}' does not exist. Please create it first in the Pinecone console.\n"
                f"Existing indexes: {', '.join(existing_indexes) if existing_indexes else 'None'}"
            )

        self.stdout.write(f"✓ Found existing index: {index_name}")

        if force_recreate:
            self.stdout.write("Clearing existing vectors...")
            index = pc.Index(index_name)
            # Delete all vectors (this might take a while for large indexes)
            index.delete(delete_all=True)
            self.stdout.write("✓ Cleared existing vectors")

        # Create vectorstore from documents
        self.stdout.write(
            "Creating vector embeddings and uploading to Pinecone...")

        vectorstore = Pinecone.from_documents(
            documents=chunks,
            embedding=embedding_model,
            index_name=index_name
        )

        self.stdout.write("✓ Vector store created successfully")
        return vectorstore
