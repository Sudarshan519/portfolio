from apps.rps_remit.otp.schema import OTP


def create_otp(email,db):
        otp=OTP(phoneOrEmail=email)
        otp.setrand()
        db.add(otp)
        db.commit()
        db.refresh(otp)
        return otp