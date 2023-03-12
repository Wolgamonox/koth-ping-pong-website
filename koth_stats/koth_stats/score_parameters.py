import json

# TODO REFACTOR ALL THE SETTINGS INTO SOME SORT OF CONFIG FILE


# DEFAULT POINTS SETTINGS
DEFAULT_ALPHA = 190
DEFAULT_BETA = 0.05
DEFAULT_SIGMA = 1.9

DEFAULT_POINTS_LAST_KING = 30


class ScoreParameters:
    """Class holding the parameters for the score."""

    def __init__(
        self,
        alpha=DEFAULT_ALPHA,
        beta=DEFAULT_BETA,
        sigma=DEFAULT_SIGMA,
        points_last_king=DEFAULT_POINTS_LAST_KING,
    ):
        self.alpha = alpha
        self.beta = beta
        self.sigma = sigma
        self.points_last_king = points_last_king

    @classmethod
    def from_file(cls, filename: str):
        """Loads score parameters from file."""
        with open(filename, "r") as file:
            try:
                params = json.load(file)

                return ScoreParameters(
                    alpha=params["alpha"],
                    beta=params["beta"],
                    sigma=params["sigma"],
                    points_last_king=params["points_last_king"],
                )
            except Exception as e:
                print(e)

                print("Error reading config file, using default parameters instead.")
                return ScoreParameters()
