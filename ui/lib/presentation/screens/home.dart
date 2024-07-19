import 'package:flutter/material.dart';
import 'package:ui/core/utils/cognito_service.dart';
import 'package:ui/presentation/screens/login_page.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  void _logout(BuildContext context) async {
    await AuthService().signOut();
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (context) => LoginPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: const Color.fromARGB(255, 219, 245, 153),
        appBar: AppBar(
          backgroundColor: const Color.fromARGB(255, 219, 245, 153),
          title: const Text('home'),
        ),
        body: Center(
          child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
            const Text('AIにレシピを考えさせよう!'),
            const SizedBox(height: 40),
            ElevatedButton(
                onPressed: () => _logout(context), child: const Text('ログアウト'))
          ]),
        ));
  }
}
