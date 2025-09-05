import { CategoryCard } from './category-card/CategoryCard';

import styles from './ShopByCategory.module.scss';

export const ShopByCategory = () => {
    const imagesByCategories = {
        Bracelet: 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748166/1_ak7nga.jpg',
        'Earring':
            'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748166/2_kg1ckf.jpg',
        Watche: 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1756919034/sbs_latestmodelpage_nmtrx2.jpg',
        Pendant: 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748165/3_ukmmmx.avif',
        Ring: 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748166/4_tmk4cj.avif',
        Necklace: 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1757059878/Generated_Image_September_05_2025_-_11_09AM_unrhyw.jpg',
    };

    return (
        <section className={styles['user-action']}>
            <h3>Shop By Category</h3>
            <ul className={styles['links']}>
                {Object.entries(imagesByCategories).map(([category, imageUrl]) => (
                    <CategoryCard
                        key={category}
                        category={category}
                        imageUrl={imageUrl}
                    />
                ))}
            </ul>
        </section>
    );
};

// import { CategoryCard } from './category-card/CategoryCard';

// import styles from './ShopByCategory.module.scss';

// export const ShopByCategory = () => {
//     const imagesByCategories = [
//         { Braclet: 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748166/1_ak7nga.jpg' },
//         {
//             'Stud Earring':
//                 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748166/2_kg1ckf.jpg',
//         },
//         {
//             Watche: 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1756919034/sbs_latestmodelpage_nmtrx2.jpg',
//         },
//         {
//             'Drop Earring':
//                 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1757008022/EdJqsYLXoAEsxjB_ax4pdf.jpg',
//         },
//         { Pendant: 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748165/3_ukmmmx.avif' },
//         { Ring: 'https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748166/4_tmk4cj.avif' },
//     ];
//     let currentIndex = 0;
//     return (
//         <section className={styles['user-action']}>
//             <h3>Shop By Category</h3>

//             <ul className={styles['links']}>
//                 {imagesByCategories.slice(currentIndex, 4).map((element) =>
//                     Object.entries(element).map(([category, imageUrl]) => (
//                         <CategoryCard key={category} category={category} imageUrl={imageUrl} />
//                     ))
//                 )}
//             </ul>
//         </section>
//     );
// };
