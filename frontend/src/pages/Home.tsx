import { Box } from "@mui/material";
import PrimaryAppBar from "./templates/PrimaryAppBar";

const Home = () => {
  return (
    <Box sx={{ display: "flex" }}>
      <PrimaryAppBar />
      <Box component="main" sx={{ p: 1 }}>
        Hello
      </Box>
    </Box>
  );
};

export default Home;
