import { Outlet, Link } from "react-router-dom";
import styles from "./Layout.module.css";
import Azure from "../../assets/Shadow Seller 180 X 180.png";
import { CopyRegular, ShareRegular } from "@fluentui/react-icons";
import { Dialog, Stack, TextField } from "@fluentui/react";
import { useEffect, useState } from "react";
import { useIsAuthenticated, useMsal } from "@azure/msal-react";
import { SignInButton } from "../../components/Signin/SignInButton";
import { SignOutButton } from "../../components/Signin/SignOutButton";

import { loginRequest } from '../../authConfig';
import { callMsGraph } from '../../graph';


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

    /**
* Renders information about the signed-in user or a button to retrieve data about the user
*/
    const ProfileContent = () => {
        const { instance, accounts } = useMsal();
        const [graphData, setGraphData] = useState(null);
        
        function RequestProfileData() {
            // Silently acquires an access token which is then attached to a request for MS Graph data
            instance
                .acquireTokenSilent({
                    ...loginRequest,
                    account: accounts[0],
                })
                .then((response) => {
                    callMsGraph(response.accessToken).then((response) => setGraphData(response));
                });
        }
        
        return (
            <>
                {accounts[0].name}
            </>
        );
    };

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
                            <h3 className={styles.headerTitle}>Shadow Seller -  {isAuthenticated ? <ProfileContent /> : "Not logged in"}</h3>
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
