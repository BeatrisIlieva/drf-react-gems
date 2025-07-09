import styles from "./PaddedContainer.module.scss";

export const PaddedContainer = ({ children, backgroundColor }) => {
    const getBackgroundClass = (bgColor) => {
        const colorMap = {
            white: styles["padded-container--white"],
            "lightest-grey": styles["padded-container--lightest-grey"],
        };
        return colorMap[bgColor] || "";
    };

    const backgroundClass = backgroundColor
        ? getBackgroundClass(backgroundColor)
        : "";
    const containerClasses = [styles["padded-container"], backgroundClass]
        .filter(Boolean)
        .join(" ");

    return <div className={containerClasses}>{children}</div>;
};
