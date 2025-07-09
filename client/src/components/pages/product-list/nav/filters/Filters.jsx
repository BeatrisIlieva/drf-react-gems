import { Icon } from "../../../../reusable/icon/Icon";

import styles from "./Filters.module.scss";
import { useProductFiltersContext } from "../../../../../contexts/ProductFiltersContext";

export const Filters = () => {
    const { toggleDisplayFilters, displayFilters } = useProductFiltersContext();

    return (
        <li className={styles["filters"]} onClick={toggleDisplayFilters}>
            <span>{displayFilters ? "hide filters" : "filters"}</span>
            <Icon name={"filter"} fontSize={0.85} />
        </li>
    );
};
