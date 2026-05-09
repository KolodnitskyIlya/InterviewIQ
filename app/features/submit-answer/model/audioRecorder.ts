import { Application, knownFolders, path, isAndroid } from "@nativescript/core";

declare const android: any;
declare const java: any;

export interface RecordedAudio {
  filePath: string;
  fileName: string;
  contentType: string;
  audioBase64: string;
}

let recorder: any | null = null;
let currentFilePath = "";

function requestAndroidMicrophonePermission(): void {
  const activity =
    Application.android?.foregroundActivity ||
    Application.android?.startActivity;
  if (!activity || !android?.Manifest?.permission?.RECORD_AUDIO) {
    return;
  }

  const permission = android.Manifest.permission.RECORD_AUDIO;
  const granted = android.content.pm.PackageManager.PERMISSION_GRANTED;
  const current = activity.checkSelfPermission(permission);
  if (current !== granted) {
    activity.requestPermissions([permission], 2101);
  }
}

function readAndroidFileAsBase64(filePath: string): string {
  const file = new java.io.File(filePath);
  const stream = new java.io.FileInputStream(file);
  const bytes = Array.create("byte", file.length());
  stream.read(bytes);
  stream.close();
  return android.util.Base64.encodeToString(bytes, android.util.Base64.NO_WRAP);
}

export function startAudioRecording(): string {
  if (!isAndroid) {
    throw new Error(
      "Voice recording is currently implemented for Android testing.",
    );
  }

  requestAndroidMicrophonePermission();

  const folder = knownFolders.documents();
  currentFilePath = path.join(folder.path, `answer-${Date.now()}.m4a`);

  recorder = new android.media.MediaRecorder();
  recorder.setAudioSource(android.media.MediaRecorder.AudioSource.MIC);
  recorder.setOutputFormat(android.media.MediaRecorder.OutputFormat.MPEG_4);
  recorder.setAudioEncoder(android.media.MediaRecorder.AudioEncoder.AAC);
  recorder.setOutputFile(currentFilePath);
  recorder.prepare();
  recorder.start();

  return currentFilePath;
}

export function stopAudioRecording(): RecordedAudio {
  if (!recorder || !currentFilePath) {
    throw new Error("Recording has not been started.");
  }

  recorder.stop();
  recorder.reset();
  recorder.release();
  recorder = null;

  const fileName = currentFilePath.split(/[\\/]/).pop() || "answer.m4a";
  return {
    filePath: currentFilePath,
    fileName,
    contentType: "audio/mp4",
    audioBase64: readAndroidFileAsBase64(currentFilePath),
  };
}

export function cancelAudioRecording(): void {
  if (!recorder) {
    return;
  }

  try {
    recorder.stop();
  } catch {}
  recorder.reset();
  recorder.release();
  recorder = null;
}
