import { configureStore } from "@reduxjs/toolkit";
import { persistStore, persistReducer, FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER } from "redux-persist";
import storage from "redux-persist/lib/storage";
import { combineReducers } from "@reduxjs/toolkit";

import authReducer from "./features/auth/authSlice.js";
import storeReducer from "./features/store/storeSlice.js";
import branchReducer from "./features/branch/branchSlice.js";
import onboardingReducer from "./features/onboarding/onboardingSlice.js";
import userReducer from "./features/user/userSlice.js";
import productReducer from "./features/product/productSlice.js";
import categoryReducer from "./features/category/categorySlice.js";
import saleReducer from "./features/sale/saleSlice.js";
import transactionReducer from "./features/transaction/transactionSlice.js";
import inventoryReducer from "./features/inventory/inventorySlice.js";
import orderReducer from "./features/order/orderSlice.js";
import customerReducer from "./features/customer/customerSlice.js";
import employeeReducer from "./features/employee/employeeSlice.js";
import cartReducer from "./features/cart/cartSlice.js";
import shiftReportReducer from "./features/shiftReport/shiftReportSlice.js";
import refundReducer from "./features/refund/refundSlice.js";
import branchAnalysisReducer from "./features/branchAnalytics/branchAnalyticsSlice.js";
import storeAnalyticsReducer from "./features/storeAnalytics/storeAnalyticsSlice.js";
import adminDashboardReducer from "./features/adminDashboard/adminDashboardSlice.js";
import subscriptionPlanReducer from "./features/subscriptionPlan/subscriptionPlanSlice.js";
import subscriptionReducer from "./features/subscription/subscriptionSlice.js";
import paymentReducer from "./features/payment/paymentSlice.js";

// ✅ Persist config cho cart — giữ lại giỏ hàng khi F5
const cartPersistConfig = {
  key: "cart",
  storage,
  whitelist: ["items", "selectedCustomer", "note", "discount", "paymentMethod", "heldOrders"],
};

// ✅ Persist config cho branch — giữ thông tin chi nhánh khi F5
const branchPersistConfig = {
  key: "branch",
  storage,
  whitelist: ["branch"],
};

// ✅ Persist config cho user — giữ profile khi F5
const userPersistConfig = {
  key: "user",
  storage,
  whitelist: ["userProfile"],
};

const rootReducer = combineReducers({
  auth: authReducer,
  store: storeReducer,
  branch: persistReducer(branchPersistConfig, branchReducer),
  onboarding: onboardingReducer,
  user: persistReducer(userPersistConfig, userReducer),
  category: categoryReducer,
  product: productReducer,
  employee: employeeReducer,
  inventory: inventoryReducer,
  order: orderReducer,
  customer: customerReducer,
  sale: saleReducer,
  transaction: transactionReducer,
  cart: persistReducer(cartPersistConfig, cartReducer),
  shiftReport: shiftReportReducer,
  refund: refundReducer,
  branchAnalytics: branchAnalysisReducer,
  storeAnalytics: storeAnalyticsReducer,
  adminDashboard: adminDashboardReducer,
  subscriptionPlan: subscriptionPlanReducer,
  subscription: subscriptionReducer,
  payment: paymentReducer,
});

const globleState = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }),
});

export const persistor = persistStore(globleState);
export default globleState;
