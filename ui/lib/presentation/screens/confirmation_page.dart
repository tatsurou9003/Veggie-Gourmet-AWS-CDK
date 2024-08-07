import 'package:flutter/material.dart';
import 'package:ui/core/utils/cognito_service.dart';
import 'home.dart';

class ConfirmationPage extends StatefulWidget {
  const ConfirmationPage(
      {super.key, required this.username, required this.email});
  final String username;
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
    if (_formKey.currentState != null && _formKey.currentState!.validate()) {
      // 確認コードの送信処理
      final confirmationCode = _confirmationCodeController.text.trim();
      try {
        bool success = await AuthService()
            .confirmSignUp(widget.username, confirmationCode);
        if (success) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('アカウントが確認されました')),
          );
          Navigator.of(context).pushReplacement(
            MaterialPageRoute(builder: (context) => Home()),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('確認できなかったのでもう一度試してね。')),
          );
        }
      } catch (e) {
        print('Confirmation error: $e');
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('エラーが発生しました: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('確認コード入力')),
      body: Form(
          key: _formKey,
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
              ElevatedButton(
                onPressed: () async {
                  try {
                    await authService.resendConfirmationCode(widget.username);
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                          content:
                              Text('${widget.email}に新しい確認コードを送信したのでメールを確認してね')),
                    );
                  } catch (e) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('確認コードの再送信に失敗しちゃった: $e')),
                    );
                  }
                },
                child: const Text('確認コードを再送信'),
              ),
            ],
          )),
    );
  }
}
