import { createBrowserRouter } from "react-router";
import { Layout } from "./components/Layout";
import { Login } from "./components/Login";
import { UploadSchedule } from "./components/UploadSchedule";
import { ScheduleView } from "./components/ScheduleView";
import { FatigueScores } from "./components/FatigueScores";
import { BurnoutForecast } from "./components/BurnoutForecast";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Login,
  },
  {
    path: "/dashboard",
    Component: Layout,
    children: [
      { index: true, Component: UploadSchedule },
      { path: "schedule", Component: ScheduleView },
      { path: "fatigue", Component: FatigueScores },
      { path: "burnout", Component: BurnoutForecast },
    ],
  },
]);