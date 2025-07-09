import { useEffect, useRef } from "react";
import { Logo } from "./logo/Logo";

import { Buttons } from "./buttons/Buttons";
import styles from "./Header.module.scss";
import { useSentinel } from "../../../hooks/useSentinel";
import { Banner } from "./banner/Banner";
import { Nav } from "../../reusable/nav/Nav";
import { navLinks } from "../../../constants/mainNavLinksData";
import { useLocation, useNavigate } from "react-router";
import { Icon } from "../../reusable/icon/Icon";

export const Header = () => {
    const headerRef = useRef(null);

    const { sentinelRef, isSticky } = useSentinel();
    const navigate = useNavigate();

    useEffect(() => {
        let lastScrollY = 0;

        const handleScroll = () => {
            const currentScrollY = window.scrollY;
            const header = headerRef.current;
            if (!header) return;

            if (currentScrollY > 0 && currentScrollY > lastScrollY) {
                header.classList.remove(styles.visible);
                header.classList.add(styles.hidden);
            } else if (currentScrollY < lastScrollY) {
                header.classList.remove(styles.hidden);
                header.classList.add(styles.visible);
            }

            lastScrollY = currentScrollY;
        };

        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    const location = useLocation();

    const getUrlSegment = () => {
        const pathname = location.pathname;

        if (pathname.includes("payment")) {
            return "Payment";
        } else if (pathname.includes("checkout")) {
            return "Checkout";
        }
        return "regular";
    };

    const segment = getUrlSegment();

    return (
        <>
            {segment === "regular" && <Banner />}

            <div ref={sentinelRef} className={styles["sentinel"]} />

            <header
                ref={headerRef}
                className={`${styles["header"]} ${
                    styles["visible"]
                } ${isSticky ? styles["sticky"] : ""}`}
            >
                {segment !== "regular" ? (
                    <div className={styles["checkout"]}>
                        <div
                            className={styles["wrapper"]}
                            onClick={() => navigate("/user/shopping-bag")}
                        >
                            <Icon
                                name="arrowLeft"
                                isSubtle={true}
                                fontSize={0.9}
                            />
                            <p>Back to Bag</p>
                        </div>
                        <Logo />
                    </div>
                ) : (
                    <>
                        <Logo />
                        <Nav links={navLinks} />
                        <Buttons />
                    </>
                )}
            </header>
        </>
    );
};
