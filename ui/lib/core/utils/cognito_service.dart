import 'package:amazon_cognito_identity_dart_2/cognito.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class AuthService {
  final userPool = CognitoUserPool(
    dotenv.env['POOL_ID']!,
    dotenv.env['CLIENT_ID']!,
  );

  // サインアップ（新規ユーザー登録）
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
    // ユーザーの登録を確認コードで確認する
  }

  // サインイン（ログイン）
  Future<CognitoUserSession?> signIn(String email, String password) async {}

  // サインアウト（ログアウト）
  Future<bool> signOut() async {
    // 現在のユーザーをログアウトさせる
  }

  // ログイン状態チェック
  Future<bool> isLoggedIn() async {
    // 現在のユーザーがログイン中かどうかを確認する
  }
}
