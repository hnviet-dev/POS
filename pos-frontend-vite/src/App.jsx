import React, { useEffect } from "react";
import { Routes, Route, Navigate } from "react-router";
import { useDispatch, useSelector } from "react-redux";

// Auth and Store Routes
import AuthRoutes from "./routes/AuthRoutes";
import StoreRoutes from "./routes/StoreRoutes";
import BranchManagerRoutes from "./routes/BranchManagerRoutes";
import { getUserProfile } from "./Redux Toolkit/features/user/userThunks";
import Landing from "./pages/common/Landing/Landing";
import CashierRoutes from "./routes/CashierRoutes";
import Onboarding from "./pages/onboarding/Onboarding";
import { getStoreByAdmin } from "./Redux Toolkit/features/store/storeThunks";
import SuperAdminRoutes from "./routes/SuperAdminRoutes";
import PageNotFound from "./pages/common/PageNotFound";
import AiChatWidget from "./components/AiChatWidget";
import StorePending from "./pages/common/StorePending";
import StoreBlocked from "./pages/common/StoreBlocked";

const App = () => {
  const dispatch = useDispatch();
  const { userProfile } = useSelector((state) => state.user);
  const { store } = useSelector((state) => state.store);

  useEffect(() => {
    const jwt = localStorage.getItem("jwt");
    if (jwt) {
      dispatch(getUserProfile(jwt));
    }
  }, [dispatch]);

  useEffect(() => {
    if (userProfile && userProfile.role === "ROLE_STORE_ADMIN") {
      dispatch(getStoreByAdmin(userProfile.jwt));
    }
  }, [dispatch, userProfile]);

  let content;

  // console.log("state ", user)

  if (userProfile && userProfile.role) {
    // User is logged in
    if (userProfile.role === "ROLE_ADMIN") {
      content = (
        <Routes>
          <Route path="/" element={<Navigate to="/super-admin" replace />} />
          <Route path="/super-admin/*" element={<SuperAdminRoutes />} />
          <Route
            path="*"
            element={<PageNotFound/>}
          />
        </Routes>
      );
    } else if (userProfile.role === "ROLE_BRANCH_CASHIER") {
      content = (
        <Routes>
          <Route path="/" element={<Navigate to="/cashier" replace />} />
          <Route path="/cashier/*" element={<CashierRoutes />} />
          <Route
            path="*"
            element={<PageNotFound/>}
          />
        </Routes>
      );
    } else if (
      userProfile.role === "ROLE_STORE_ADMIN" ||
      userProfile.role === "ROLE_STORE_MANAGER"
    ) {
      if (!store) {
        // Chưa có store → vào onboarding tạo store
        content = (
          <Routes>
            <Route path="/auth/onboarding" element={<Onboarding />} />
            <Route
              path="*"
              element={<PageNotFound/>}
            />
          </Routes>
        );
        return content;
      } else if (store.status === "PENDING") {
        // Store đang chờ duyệt
        content = (
          <Routes>
            <Route path="/" element={<Navigate to="/store-pending" replace />} />
            <Route path="/store-pending" element={<StorePending />} />
            <Route path="*" element={<Navigate to="/store-pending" replace />} />
          </Routes>
        );
      } else if (store.status === "BLOCKED") {
        // Store bị từ chối / khóa
        content = (
          <Routes>
            <Route path="/" element={<Navigate to="/store-blocked" replace />} />
            <Route path="/store-blocked" element={<StoreBlocked />} />
            <Route path="*" element={<Navigate to="/store-blocked" replace />} />
          </Routes>
        );
      } else {
        // Store ACTIVE → vào dashboard bình thường
        content = (
          <Routes>
            <Route path="/" element={<Navigate to="/store" replace />} />
            <Route path="/store/*" element={<StoreRoutes />} />
            <Route
              path="*"
              element={<PageNotFound/>}
            />
          </Routes>
        );
      }
    } else if (
      userProfile.role === "ROLE_BRANCH_MANAGER" ||
      userProfile.role === "ROLE_BRANCH_ADMIN"
    ) {
      content = (
        <Routes>
          <Route path="/" element={<Navigate to="/branch" replace />} />
          <Route path="/branch/*" element={<BranchManagerRoutes />} />
          <Route
            path="*"
            element={<PageNotFound/>}
          />
        </Routes>
      );
    } else {
      // Unknown role, redirect to landing or error page
      content = (
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route
            path="*"
            element={ <PageNotFound/>}
          />
        </Routes>
      );
    }
  } else {
    // User is not logged in, show landing page and auth routes
    content = (
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/auth/*" element={<AuthRoutes />} />
        <Route
          path="*"
          element={
          <PageNotFound/>
          }
        />
      </Routes>
    );
  }

  return (
    <>
      {content}
      {/* AI Chatbot — hiển thị cho tất cả user đã đăng nhập */}
      {userProfile && userProfile.role && <AiChatWidget />}
    </>
  );
};

export default App;
