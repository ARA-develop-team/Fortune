from project import Fortune
from src.parse_arguments import parse_arguments

"""           FORTUNE            """
"""   ARA Development present    """
"""  First cryptography project  """

"""  Version 0.0.0               """
"""  Launched: 7 okt 2022        """


def main():
    args_dict = parse_arguments()
    fortune = Fortune(**args_dict)

    fortune.run()

    # fortune.train_predictor()
    
    # fortune.test_predictor()


if __name__ == "__main__":
    main()
