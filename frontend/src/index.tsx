import React from "react";
import ReactDOM from "react-dom/client";
import { HashRouter, Routes, Route } from "react-router-dom";
import { initializeIcons } from "@fluentui/react";

import { PublicClientApplication } from '@azure/msal-browser';
import { MsalProvider } from '@azure/msal-react';
import { msalConfig } from './authConfig';

// Bootstrap components
import 'bootstrap/dist/css/bootstrap.min.css';

const msalInstance = new PublicClientApplication(msalConfig);

import "./index.css";

import Layout from "./pages/layout/Layout";
import NoPage from "./pages/NoPage";
import Chat from "./pages/chat/Chat";

initializeIcons();

export default function App() {
    return (
        <HashRouter>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<Chat />} />
                    <Route path="*" element={<NoPage />} />
                </Route>
            </Routes>
        </HashRouter>
    );
}

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
    <React.StrictMode>
        <MsalProvider instance={msalInstance}>
        <App />
        </MsalProvider>
    </React.StrictMode>
);
