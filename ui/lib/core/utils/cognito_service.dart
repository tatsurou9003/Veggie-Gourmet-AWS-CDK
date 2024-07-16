import 'package:amazon_cognito_identity_dart_2/cognito.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

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
      return result.userConfirmed ?? false;
    } catch (e) {
      print('Error: $e');
    }
    return false;
  }

  // サインアップ確認
  Future<bool> confirmSignUp(String email, String confirmationCode) async {
    final cognitoUser = CognitoUser(email, userPool);
    try {
      return await cognitoUser.confirmRegistration(confirmationCode);
    } catch (e) {
      print('Error: $e');
      return false;
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
