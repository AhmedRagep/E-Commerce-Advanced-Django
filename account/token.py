# - Import password reset token generator

# انشاء رموز استعادة علمات المرور
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# 
# لدعم الدوال المتقدمة
from django.utils import six


# - Password reset token generator method

class UserVerificationTokenGenerator(PasswordResetTokenGenerator):
    
    # يتم جلب وتحويل القيم الي نص لامان وتوافق المعلومات
    def _make_hash_value(self, user, timestamp):
        
        # لجلب رقم اليوزر وتحويله الي نص بغض النظر عن الاصدار
        user_id = six.text_type(user.pk)

        # لجلب الوقت في اللحظه الحالية عند انشاء الطلب وتحويله الي نص
        ts = six.text_type(timestamp)

        # جلب اليوزر النشط وتحويله الي نص
        is_active = six.text_type(user.is_active)

        # دمج البيانات وارسالها معا
        return f"{user_id}{ts}{is_active}"

user_tokenizer_generate = UserVerificationTokenGenerator()