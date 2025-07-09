import { useMemo } from "react";
import { useParams } from "react-router";

export const useCategoryName = () => {
    const { categoryName } = useParams();

    const { capitalizedPlural, capitalizedSingular } = useMemo(() => {
        if (!categoryName) {
            return {
                capitalizedPlural: undefined,
                capitalizedSingular: undefined,
            };
        }

        const capitalized =
            categoryName.charAt(0).toUpperCase() + categoryName.slice(1);
        const singular = capitalized.slice(0, -1);

        return {
            capitalizedPlural: capitalized,
            capitalizedSingular: singular,
        };
    }, [categoryName]);

    return {
        categoryName,
        categoryNameCapitalizedPlural: capitalizedPlural,
        categoryNameCapitalizedSingular: capitalizedSingular,
    };
};
