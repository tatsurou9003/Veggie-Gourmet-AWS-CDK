import 'package:flutter/material.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text('home'),
        ),
        body: Center(
          child: Column(children: [
            const Text('AIにレシピを考えさせよう!'),
            ElevatedButton(onPressed: () {}, child: const Text('ログアウト'))
          ]),
        ));
  }
}
