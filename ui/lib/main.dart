import 'package:flutter/material.dart';
import 'package:ui/presentation/screens/home.dart';
import 'package:ui/presentation/screens/login_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Veggie Gourmet',
      debugShowCheckedModeBanner: false,
      theme:
          ThemeData(primarySwatch: Colors.lightGreen, fontFamily: 'NotoSansJP'),
      home: LoginPage(),
    );
  }
}
