import { CssBaseline, ThemeProvider } from "@mui/material";
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
import Home from "./pages/Home";
import Games from "./pages/Games";
import createMuiTheme from "./theme/theme";

const router = createBrowserRouter(
  createRoutesFromElements([
    <Route path="/" element={<Home />}></Route>,
    <Route path="/games" element={<Games />}></Route>,
  ])
);

const App: React.FC = () => {
  const theme = createMuiTheme();
  return (
    <>
      <CssBaseline />
      <ThemeProvider theme={theme}>
        <RouterProvider router={router} />
      </ThemeProvider>
    </>
  );
};

export default App;
