from wizard.config import settings


def main():
    print("Wizard configuration loaded.")
    print(f"Environment: {settings.environment}")
    print(f"Log level: {settings.log_level}")


if __name__ == "__main__":
    main()