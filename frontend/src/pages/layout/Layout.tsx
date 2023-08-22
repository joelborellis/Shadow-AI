import { Outlet, Link, NavLink } from "react-router-dom";
import styles from "./Layout.module.css";
import { useState } from "react";

import { useIsAuthenticated, useMsal } from "@azure/msal-react";
import { SignInButton } from "../../components/Signin/SignInButton";
import { SignOutButton } from "../../components/Signin/SignOutButton";
import { SettingsButton } from "../../components/Settings/SettingsButton";
import { GraphContent } from "../../components/Signin/GraphContent";
import { Panel, Stack } from "@fluentui/react";
import { Checkbox, CheckboxProps, Divider, Label } from "@fluentui/react-components";

const Layout = (props: any) => {
  const isAuthenticated = useIsAuthenticated();
  const [isSettingsOpen, setIsSettingsOpen] = useState<boolean>(false);
  const [checked, setChecked] = useState<CheckboxProps["checked"]>(true);

  const dismissSettings = async () => {
    alert(checked);
    setIsSettingsOpen(false);
  };

  const openSettings = async () => {
    setIsSettingsOpen(true);
  };

  return (
    <div className={styles.layout}>
      <header className={styles.header} role={"banner"}>
        <div className={styles.headerContainer}>
          <Stack horizontal verticalAlign="center">
            <Link to="/" className={styles.headerTitleContainer}>
              <h3 className={styles.headerTitle}>
                Shadow Seller -{" "}
                {isAuthenticated ? <GraphContent /> : "Not logged in"}
              </h3>
            </Link>

            
            <h3 className={styles.headerAdviceTitle}>
                  <NavLink
                    to="/chat2"
                    className={({ isActive }) =>
                      isActive
                        ? styles.headerNavPageLinkActive
                        : styles.headerNavPageLink
                    }
                  >
                    Advice
                  </NavLink>
                  </h3>

                  <h3 className={styles.headerInformationTitle}>
                  <NavLink
                    to="/chat3"
                    className={({ isActive }) =>
                      isActive
                        ? styles.headerNavPageLinkActive
                        : styles.headerNavPageLink
                    }
                  >
                    Information
                  </NavLink>
                  </h3>

                  <h3 className={styles.headerSuggestionTitle}>
                  <NavLink
                    to="/chat4"
                    className={({ isActive }) =>
                      isActive
                        ? styles.headerNavPageLinkActive
                        : styles.headerNavPageLink
                    }
                  >
                    Suggestions
                  </NavLink>
                  </h3>
              
            

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
