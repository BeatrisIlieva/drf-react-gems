import styles from "./Skeleton.module.scss";

export const Skeleton = () => {
    return (
        <div className={styles["loading-container"]}>
            {Array.from({ length: 3 }).map((_, index) => (
                <div key={index} className={styles["skeleton-item"]}>
                    <div className={styles["skeleton-image"]}></div>
                    <div className={styles["skeleton-content"]}>
                        <div
                            className={`${styles["skeleton-text"]} ${styles["medium"]}`}
                        ></div>
                        <div
                            className={`${styles["skeleton-text"]} ${styles["long"]}`}
                        ></div>
                        <div
                            className={`${styles["skeleton-text"]} ${styles["short"]}`}
                        ></div>
                        <div className={styles["skeleton-actions"]}>
                            <div className={styles["skeleton-button"]}></div>
                            <div className={styles["skeleton-quantity"]}></div>
                        </div>
                    </div>
                    <div className={styles["skeleton-price"]}></div>
                </div>
            ))}
        </div>
    );
};
