import { useProductContext } from '../../../../../../contexts/ProductContext';
import { CategoryItem } from './category-item/CategoryItem';

export const CategorySelector = () => {
    const { categoriesData } = useProductContext();

    return (
        <>
            {categoriesData.length > 0 &&
                categoriesData.map((item) => <CategoryItem key={item.reference__id} {...item} />)}
        </>
    );
};
