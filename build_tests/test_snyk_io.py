import hashlib
import sh


def get_sha1(filename):
    """Get a sha1 for a file

    Args:
        filename: Path to the file

    Returns:
        Sha1 string of the file
    """
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    sha1 = hashlib.sha1()

    with open(filename, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()


def pypi_mirror_always_trailing_slash(filename):

    with open(filename, mode="r") as file:
        data = file.readlines()

    trailing_slash = data[0].endswith("/\n")

    if not trailing_slash:
        print("Adding the trailing slash to the first line of the %s" % filename)
        data[0] = data[0].replace("\n", "/\n")
        with open(filename, "w") as file:
            file.writelines(data)


def test_snyk_io__prerequisites():
    """Verify that the Pipfile.lock matches the requirements.txt.

    Snyk.io cannot look in the Pipfile.lock for vulnerabilities.
    """
    filename = "requirements.txt"
    sha_before = get_sha1(filename)
    sh.make("create-requirements-txt")
    pypi_mirror_always_trailing_slash(filename)
    sha_after = get_sha1(filename)
    assert sha_before == sha_after
