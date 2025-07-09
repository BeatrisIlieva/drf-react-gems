import styles from "./AuthLayout.module.scss";

export const AuthLayout = ({ children }) => {
    return (
        <section className={styles["auth-layout"]}>
            <div className={styles["thumbnail"]}>
                <img
                    src="https://res.cloudinary.com/dpgvbozrb/image/upload/v1750782646/featuredimage_emerald_o6ujhw_zebbsq.png"
                    alt="necklace-image"
                />
            </div>
            <div className={styles["form"]}>{children}</div>
        </section>
    );
};
