import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { PaginatedProducts, Product } from '../types/product';

@Component({
    selector: 'app-products-list',
    templateUrl: './products-list.component.html',
    styleUrls: ['./products-list.component.css'],
})
export class ProductsListComponent implements OnInit {
    products: Product[] | null = null;
    isLoading: Boolean = true; 

    constructor(private api: ApiService) {}

    ngOnInit(): void {
      this.api.getProducts().subscribe(products => {
        console.log(products)
        this.products = products.results;
        this.isLoading = false;
      })
    }
}
