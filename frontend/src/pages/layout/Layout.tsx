import { Outlet, Link } from "react-router-dom";
import styles from "./Layout.module.css";
import Azure from "../../assets/Shadow Seller 180 X 180.png";
import { CopyRegular, ShareRegular } from "@fluentui/react-icons";
import { Dialog, Stack, TextField } from "@fluentui/react";
import { useEffect, useState } from "react";
import { useIsAuthenticated } from "@azure/msal-react";
import { SignInButton } from "../../components/Signin/SignInButton";
import { SignOutButton } from "../../components/Signin/SignOutButton";

const Layout = (props: any) => {
    const [isSharePanelOpen, setIsSharePanelOpen] = useState<boolean>(false);
    const [copyClicked, setCopyClicked] = useState<boolean>(false);
    const [copyText, setCopyText] = useState<string>("Copy URL");
    const isAuthenticated = useIsAuthenticated();
    

    const handleShareClick = () => {
        setIsSharePanelOpen(true);
    };

    const handleSharePanelDismiss = () => {
        setIsSharePanelOpen(false);
        setCopyClicked(false);
        setCopyText("Copy URL");
    };

    const handleCopyClick = () => {
        navigator.clipboard.writeText(window.location.href);
        setCopyClicked(true);
    };

    useEffect(() => {
        if (copyClicked) {
            setCopyText("Copied URL");
        }
    }, [copyClicked]);

    return (
        <div className={styles.layout}>
            <header className={styles.header} role={"banner"}>
                <div className={styles.headerContainer}>
                    <Stack horizontal verticalAlign="center">
                        {/*
                        <img
                            src={Azure}
                            className={styles.headerIcon}
                            aria-hidden="true"
                        />  
                        */}                
                        <Link to="/" className={styles.headerTitleContainer}>
                            <h3 className={styles.headerTitle}>Shadow Seller - </h3>{props.children}
                        </Link>
                        <div className={styles.shareButtonContainer}>
                            {isAuthenticated ? <SignOutButton /> : <SignInButton />}
                        </div>
                    </Stack>
                </div>
            </header>
            <Outlet />

        </div>
    );
};

export default Layout;
