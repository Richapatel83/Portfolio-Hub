import os
import pyotp


unauthorized_msg = {
    "success": False,
    "message": "You are not authorized to access this route."
}


def generate_security_qr():
    """
    Generates a QR code for the user to scan with their 2FA app.
    Only use this when running locally or when you can access the machine running this code.
    This will generate a temporary QR code image and then delete it after it is displayed.
    Just copy the key from the image and paste it into an environment variable called TOTP_KEY.
    Use a mobile 2FA app to scan the QR and access the admin routes.
    """

    key = pyotp.random_base32()
    url = pyotp.totp.TOTP(key).provisioning_uri(name="MCUxDaredevil", issuer_name="Project Tracker API")
    qr = segno.make_qr(url)
    try:
        pyclip.copy(key)
    except pyclip.base.ClipboardException:
        print("Failed to copy key to clipboard.")
    filename = f"./{key}.png"
    qr.save(filename, scale=15, light="#feffff")
    img = mpimg.imread(filename)
    plt.title(f"Key: {key}")
    plt.suptitle("Press Q to exit\n")
    plt.imshow(img)
    axes = plt.gca()
    axes.get_xaxis().set_visible(False)
    axes.get_yaxis().set_visible(False)
    plt.show()
    os.remove(filename)


def authenticate_otp(otp):
    """Authenticate an OTP using the secret key provided."""
    return pyotp.TOTP(os.getenv("TOTP_KEY")).verify(otp)


if __name__ == '__main__':
    import pyclip
    import segno
    from matplotlib import pyplot as plt
    from matplotlib import image as mpimg
    generate_security_qr()
