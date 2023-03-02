import 'package:flutter/cupertino.dart';
import 'package:macos_ui/macos_ui.dart';
import 'package:mudara_liska/main.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class RecognitionOutput {
  final String input;
  final String output;

  const RecognitionOutput({
    required this.input,
    required this.output,
  });

  factory RecognitionOutput.fromJson(Map<String, dynamic> json) {
    return RecognitionOutput(
      input: utf8.decode(json['prompt'].runes.toList()),
      output: utf8.decode(json['output'].runes.toList()),
    );
  }
}

class _HomePageState extends State<HomePage> {
  bool loading = false;
  Future<RecognitionOutput> recognizeMic(String inputType, String text) async {
    loading = true;
    final response = await http.post(Uri.parse('http://127.0.0.1:8000'),
        body:
            jsonEncode(<String, String>{"inputType": inputType, "text": text}),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        });
    if (response.statusCode == 200) {
      loading = false;
      return RecognitionOutput.fromJson(jsonDecode(response.body));
    } else {
      print('Failed to load!');
      loading = false;
      return RecognitionOutput(input: input, output: "Něšto je so nimokuliwo.");
    }
  }

  void recognize(String inputType, String text) async {
    if (loading) {
      print("loading");
      return;
    } else {
      recognizeMic(inputType, text).then((value) => {
            setState(
              () {
                input = value.input;
                output = value.output;
              },
            )
          });
    }
  }

  final promptController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return SizedBox(
        width: MediaQuery.of(context).size.width,
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            children: [
              Expanded(
                  child: Column(
                children: [
                  const Text(
                    "Mudra Liška",
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                  Padding(
                    padding: const EdgeInsets.only(top: 16),
                    child: Column(
                      children: [
                        Align(
                          alignment: Alignment.topRight,
                          child: Text(input),
                        ),
                        Align(
                          alignment: Alignment.topLeft,
                          child: Text(output),
                        ),
                      ],
                    ),
                  )
                ],
              )),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Row(
                  children: [
                    Flexible(
                      flex: 1,
                      child: MacosTextField(
                        controller: promptController,
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.fromLTRB(8, 0, 0, 0),
                      child: MacosIconButton(
                        icon: const MacosIcon(CupertinoIcons.mic_circle),
                        onPressed: () => {recognize("mic", "")},
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.fromLTRB(8, 0, 0, 0),
                      child: MacosIconButton(
                        icon: const MacosIcon(CupertinoIcons.search),
                        onPressed: () =>
                            recognize("text", promptController.text),
                      ),
                    )
                  ],
                ),
              )
            ],
          ),
        ));
  }
}
