import { useProductListContext } from '../../../../../../contexts/ProductListContext';
import { CategoryItem } from './category-item/CategoryItem';

export const CategorySelector = () => {
    const { categoriesData } = useProductListContext();

    return (
        <>
            {categoriesData.length > 0 &&
                categoriesData.map((item) => <CategoryItem key={item.reference__id} {...item} />)}
        </>
    );
};
