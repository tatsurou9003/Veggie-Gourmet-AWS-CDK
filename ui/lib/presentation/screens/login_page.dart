import 'package:flutter/material.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text('ログイン'),
        ),
        body: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                decoration: InputDecoration(labelText: 'Email'),
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'PassWord'),
              ),
              const SizedBox(
                height: 40,
              ),
              ElevatedButton(onPressed: () {}, child: Text('ログイン')),
              TextButton(
                  onPressed: () {}, child: Text('Need an account? Sign up'))
            ],
          ),
        ));
  }
}
