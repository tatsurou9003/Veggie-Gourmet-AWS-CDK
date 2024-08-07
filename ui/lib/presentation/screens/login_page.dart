import 'package:flutter/material.dart';
import 'package:ui/core/utils/cognito_service.dart';
import 'package:ui/presentation/screens/home.dart';
import 'package:ui/presentation/screens/confirmation_page.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final authService = AuthService();
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLogin = true;
  bool _isLoading = false;

  @override
  void dispose() {
    _usernameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _submitForm() async {
    if (_formKey.currentState!.validate()) {
      setState(() {
        _isLoading = true;
      });
      try {
        final username = _usernameController.text;
        final email = _emailController.text;
        final password = _passwordController.text;

        if (_isLogin) {
          final session = await authService.signIn(username, password);
          if (session != null) {
            Navigator.of(context).pushReplacement(
              MaterialPageRoute(
                builder: (context) => Home(),
              ),
            );
          } else {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('ログインに失敗しました')),
            );
          }
        } else {
          final signUpResult =
              await authService.signUp(username, email, password);
          if (signUpResult) {
            Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) =>
                    ConfirmationPage(username: username, email: email),
              ),
            );
          } else {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('サインアップに失敗しました')),
            );
          }
        }
      } finally {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  String? _validatePassword(String? value) {
    if (value == null || value.isEmpty) {
      return 'パスワードを入力してね';
    }
    if (value.length < 8) {
      return 'パスワードは8文字以上にしてね';
    }
    if (!value.contains(RegExp(r'[A-Z]'))) {
      return 'パスワードには大文字を含めてね';
    }
    if (!value.contains(RegExp(r'[a-z]'))) {
      return 'パスワードには小文字を含めてね';
    }
    if (!value.contains(RegExp(r'[0-9]'))) {
      return 'パスワードには数字を含めてね';
    }
    if (!value.contains(RegExp(r'[!@#$%^&*(),.?":{}|<>]'))) {
      return 'パスワードには特殊文字を含めてね';
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: const Color.fromARGB(255, 219, 245, 153),
        appBar: AppBar(
          title: Text(_isLogin ? 'ログイン' : 'サインアップ'),
          backgroundColor: const Color.fromARGB(255, 219, 245, 153),
        ),
        body: _isLoading
            ? const Center(child: CircularProgressIndicator())
            : Form(
                key: _formKey,
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: SingleChildScrollView(
                    child: Column(
                      children: [
                        TextFormField(
                            controller: _usernameController,
                            decoration:
                                const InputDecoration(labelText: 'ユーザー名'),
                            validator: (value) {
                              if (value == null || value.isEmpty) {
                                return 'ユーザー名を入力してね';
                              }
                            }),
                        const SizedBox(height: 20),
                        TextFormField(
                            controller: _passwordController,
                            decoration: const InputDecoration(
                              labelText: 'パスワード',
                            ),
                            obscureText: true,
                            validator: (value) {
                              if (value == null || value.isEmpty) {
                                return 'パスワードを入力してね';
                              }
                            }),
                        if (!_isLogin) ...[
                          const SizedBox(height: 20),
                          TextFormField(
                              decoration: const InputDecoration(
                                  labelText: 'パスワード（確認）',
                                  helperText: '8文字以上、大文字・小文字・数字・特殊文字を含めてね'),
                              obscureText: true,
                              validator: _validatePassword),
                          const SizedBox(height: 20),
                          TextFormField(
                            controller: _emailController,
                            decoration:
                                const InputDecoration(labelText: 'メールアドレス'),
                            keyboardType: TextInputType.emailAddress,
                            validator: (value) {
                              if (value == null || value.isEmpty) {
                                return 'メールアドレスを入力してね';
                              }
                              if (!value.contains('@') ||
                                  !value.contains('.')) {
                                return '正しいメールアドレスを入力してね';
                              }
                              return null;
                            },
                          ),
                          const SizedBox(height: 20),
                        ],
                        const SizedBox(height: 40),
                        ElevatedButton(
                          onPressed: _submitForm,
                          child: Text(_isLogin ? 'ログイン' : 'サインアップ'),
                        ),
                        TextButton(
                          onPressed: () {
                            setState(() {
                              _isLogin = !_isLogin;
                            });
                          },
                          child: Text(_isLogin
                              ? 'アカウント持ってないの? サインアップしてね'
                              : 'アカウント持ってるの? ログインしてね'),
                        )
                      ],
                    ),
                  ),
                ),
              ));
  }
}
