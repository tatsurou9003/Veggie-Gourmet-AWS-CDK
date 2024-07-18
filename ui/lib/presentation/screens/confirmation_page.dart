import 'package:flutter/material.dart';
import 'package:ui/core/utils/cognito_service.dart';
import 'login_page.dart';

class ConfirmationPage extends StatefulWidget {
  const ConfirmationPage({super.key, required this.email});
  final String email;

  @override
  State<ConfirmationPage> createState() => _ConfirmationPageState();
}

class _ConfirmationPageState extends State<ConfirmationPage> {
  final authService = AuthService();
  final _formKey = GlobalKey<FormState>();
  final _confirmationCodeController = TextEditingController();

  @override
  void dispose() {
    _confirmationCodeController.dispose();
    super.dispose();
  }

  void _submitConfirmationCode() async {
    if (_formKey.currentState!.validate()) {
      final confirmationCode = _confirmationCodeController.text;
      final confirmationSuccessful =
          await authService.confirmSignUp(widget.email, confirmationCode);

      if (confirmationSuccessful) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('アカウントの確認が完了しました')),
        );
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
            builder: (context) => LoginPage(),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('確認コードが正しくありません。もう一度お試しください。')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('確認コード入力')),
      body: Form(
          child: Column(
        children: [
          Text(
            '${widget.email}に送信された確認コードを入力してね',
            style: const TextStyle(fontSize: 16),
          ),
          const SizedBox(height: 20),
          TextFormField(
            controller: _confirmationCodeController,
            decoration: const InputDecoration(labelText: '確認コード'),
            keyboardType: TextInputType.number,
            validator: (value) {
              if (value == null || value.isEmpty) {
                return '確認コードを入力してね';
              }
              return null;
            },
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: _submitConfirmationCode,
            child: const Text('確認コードを送信'),
          ),
        ],
      )),
    );
  }
}
