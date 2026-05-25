import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { BrowserRouter } from "react-router";
import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";
import globleState, { persistor } from "./Redux Toolkit/globleState.js";
import { Toaster } from "@/components/ui/use-toast";
import { ThemeProvider } from "@/components/theme-provider";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <Provider store={globleState}>
        {/* PersistGate đợi dữ liệu từ localStorage load xong trước khi render */}
        <PersistGate loading={null} persistor={persistor}>
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            <App />
            <Toaster />
          </ThemeProvider>
        </PersistGate>
      </Provider>
    </BrowserRouter>
  </StrictMode>
);
