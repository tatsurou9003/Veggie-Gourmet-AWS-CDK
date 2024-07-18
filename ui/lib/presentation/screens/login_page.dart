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
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLogin = true;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _submitForm() async {
    if (_formKey.currentState!.validate()) {
      final email = _emailController.text;
      final password = _passwordController.text;

      if (_isLogin) {
        final session = await authService.signIn(email, password);
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
        final signUpSuccessful = await authService.signUp(email, password);
        if (signUpSuccessful) {
          Navigator.of(context).push(
            MaterialPageRoute(
              builder: (context) => ConfirmationPage(
                email: email,
              ),
            ),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('サインアップに失敗しました')),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: const Color.fromARGB(255, 219, 245, 153),
        appBar: AppBar(
          title: Text(_isLogin ? 'Login' : 'Sign Up'),
        ),
        body: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _emailController,
                decoration: const InputDecoration(labelText: 'Email'),
                keyboardType: TextInputType.emailAddress,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'メールアドレスを入力してください';
                  }
                  if (!value.contains('@') || !value.contains('.')) {
                    return '正しいメールアドレスを入力してね';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              TextFormField(
                controller: _passwordController,
                decoration: const InputDecoration(labelText: 'Password'),
                obscureText: true,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'パスワードを入力してください';
                  }
                  if (value.length < 8) {
                    return 'パスワードは8文字以上である必要があります';
                  }
                  return null;
                },
              ),
              const SizedBox(
                height: 40,
              ),
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
        ));
  }
}
