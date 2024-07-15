import 'package:flutter/material.dart';

class Home extends StatelessWidget {
  const Home({super.key});

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
            ElevatedButton(onPressed: () {}, child: const Text('ログアウト'))
          ]),
        ));
  }
}
