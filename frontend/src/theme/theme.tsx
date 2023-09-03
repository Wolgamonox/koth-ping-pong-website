import { createTheme, responsiveFontSizes } from "@mui/material";

export const createMuiTheme = () => {
  let theme = createTheme({
    typography: {
      fontFamily: ["Oswald", "sans-serif"].join(","),
    },
    components: {
      MuiAppBar: {
        defaultProps: {
          color: "default",
          elevation: 0,
        },
      },
    },
  });

  theme = responsiveFontSizes(theme);
  return theme;
};

export default createMuiTheme;
