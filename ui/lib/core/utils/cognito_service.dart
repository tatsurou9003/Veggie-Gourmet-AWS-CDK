import 'package:amazon_cognito_identity_dart_2/cognito.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class SignUpResult {
  final bool success;
  final String? errorMessage;

  SignUpResult({required this.success, this.errorMessage});
}

class AuthService {
  final userPool = CognitoUserPool(
    dotenv.env['POOL_ID']!,
    dotenv.env['CLIENT_ID']!,
  );

  // サインアップ
  Future<bool> signUp(String email, String password) async {
    try {
      final userAttributes = [
        AttributeArg(name: 'email', value: email),
      ];
      final result = await userPool.signUp(email, password,
          userAttributes: userAttributes);
      print("Sign up successful: $result");
      return true;
    } catch (e) {
      print("Sign up error: $e");
      return false;
    }
  }

  // サインアップ確認
  Future<bool> confirmSignUp(String email, String confirmationCode) async {
    try {
      final cognitoUser = CognitoUser(email, userPool);
      final result = await cognitoUser.confirmRegistration(confirmationCode);
      return result;
    } catch (e) {
      if (e is CognitoClientException) {
        print("エラー: ${e.message}, code: ${e.code}, name: ${e.name}");
      } else {
        print("Unknownエラー: $e");
      }
      return false;
    }
  }

  // 確認コード再送信
  Future<void> resendConfirmationCode(String email) async {
    print("Attempting to resend confirmation code to: $email");
    try {
      final cognitoUser = CognitoUser(email, userPool);
      final result = await cognitoUser.resendConfirmationCode();
      print("Resend confirmation code result: $result");
    } catch (e) {
      print("Error resending confirmation code: $e");
      throw e;
    }
  }

  // サインイン（ログイン）
  Future<CognitoUserSession?> signIn(String email, String password) async {
    try {
      final cognitoUser = CognitoUser(email, userPool);
      final authDetails = AuthenticationDetails(
        username: email,
        password: password,
      );
      final session = await cognitoUser.authenticateUser(authDetails);
      return session;
    } catch (e) {
      print('Sign in failed: $e');
      return null;
    }
  }

  // サインアウト（ログアウト）
  Future<bool> signOut() async {
    try {
      final cognitoUser = await userPool.getCurrentUser();
      if (cognitoUser != null) {
        await cognitoUser.signOut();
        return true;
      }
      return false;
    } catch (e) {
      print('Sign out failed: $e');
      return false;
    }
  }

  // ログイン状態チェック
  Future<bool> isLoggedIn() async {
    final cognitoUser = await userPool.getCurrentUser();
    if (cognitoUser == null) {
      return false;
    }
    try {
      final session = await cognitoUser.getSession();
      return session!.isValid();
    } catch (e) {
      print(e);
      return false;
    }
  }
}
