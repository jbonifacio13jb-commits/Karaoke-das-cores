package br.com.ursoplayer.karaoke;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.res.Configuration;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.DocumentsContract;
import android.provider.DocumentsContract.Document;
import android.util.Base64;
import android.view.KeyEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.FrameLayout;
import android.widget.Toast;
import android.webkit.ConsoleMessage;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebChromeClient.FileChooserParams;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import org.json.JSONArray;
import org.json.JSONObject;

public class MainActivity extends Activity {
    private static final int PICK_FILES = 4102;
    private static final int PICK_FOLDER = 4103;
    private WebView webView;
    private volatile boolean rockDoidoActive;
    private ValueCallback<Uri[]> fileCallback;
    private View fullscreenView;
    private WebChromeClient.CustomViewCallback fullscreenCallback;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        getWindow().setStatusBarColor(0xff050508);
        getWindow().setNavigationBarColor(0xff050508);
        webView = new WebView(this);
        webView.setBackgroundColor(0xff050508);
        webView.setLayerType(View.LAYER_TYPE_HARDWARE, null);
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        s.setSupportZoom(false);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);
        s.setJavaScriptCanOpenWindowsAutomatically(false);
        s.setLoadsImagesAutomatically(true);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE);
        webView.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest req) {
                Uri u = req.getUrl();
                String scheme = u.getScheme();
                if ("file".equals(scheme) || "https".equals(scheme) || "http".equals(scheme) || "content".equals(scheme)) return false;
                try { startActivity(new Intent(Intent.ACTION_VIEW, u)); } catch (Exception ignored) {}
                return true;
            }
        });
        webView.addJavascriptInterface(new AndroidHost(), "AndroidHost");
        webView.setWebChromeClient(new WebChromeClient() {
            @Override public void onShowCustomView(View view, CustomViewCallback callback) {
                if (fullscreenView != null) { callback.onCustomViewHidden(); return; }
                fullscreenView = view;
                fullscreenCallback = callback;
                View decor = getWindow().getDecorView();
                if (decor instanceof ViewGroup) {
                    ((ViewGroup) decor).addView(view, new FrameLayout.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
                }
                enterImmersive();
            }
            @Override public void onHideCustomView() { hideFullscreenView(); }
            @Override public boolean onShowFileChooser(WebView v, ValueCallback<Uri[]> cb, FileChooserParams params) {
                if (fileCallback != null) fileCallback.onReceiveValue(null);
                fileCallback = cb;
                Intent pick = new Intent(Intent.ACTION_OPEN_DOCUMENT);
                pick.addCategory(Intent.CATEGORY_OPENABLE);
                pick.setType("*/*");
                pick.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
                pick.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);
                try { startActivityForResult(pick, PICK_FILES); }
                catch (ActivityNotFoundException e) {
                    fileCallback = null; cb.onReceiveValue(null);
                    Toast.makeText(MainActivity.this, "Não foi possível abrir o seletor de arquivos.", Toast.LENGTH_LONG).show();
                }
                return true;
            }
            @Override public boolean onConsoleMessage(ConsoleMessage m) { return true; }
        });
        setContentView(webView);
        enterImmersive();
        if (state == null) webView.loadUrl("file:///android_asset/index.html");
        else webView.restoreState(state);
    }

    public final class AndroidHost {
        @JavascriptInterface public boolean isTelevision() {
            int mode = getResources().getConfiguration().uiMode & Configuration.UI_MODE_TYPE_MASK;
            return mode == Configuration.UI_MODE_TYPE_TELEVISION || getPackageManager().hasSystemFeature("android.software.leanback");
        }
        @JavascriptInterface public String getDeviceKind() {
            if (isTelevision()) return "tv";
            return getResources().getConfiguration().smallestScreenWidthDp >= 600 ? "tablet" : "phone";
        }
        @JavascriptInterface public int getAndroidApiLevel() { return android.os.Build.VERSION.SDK_INT; }
        @JavascriptInterface public void setRockDoidoActive(boolean active) { rockDoidoActive = active; }
        @JavascriptInterface public void setOrientation(int orientation) {
            final int requested = orientation;
            runOnUiThread(new Runnable() {
                @Override public void run() { if (requested == 0 || requested == 1) setRequestedOrientation(requested); }
            });
        }
        @JavascriptInterface public void chooseFolder() {
            runOnUiThread(new Runnable() {
                @Override public void run() {
                    Intent pick = new Intent(Intent.ACTION_OPEN_DOCUMENT_TREE);
                    pick.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION);
                    try { startActivityForResult(pick, PICK_FOLDER); }
                    catch (ActivityNotFoundException e) { Toast.makeText(MainActivity.this, "O seletor de pastas não está disponível neste aparelho.", Toast.LENGTH_LONG).show(); }
                }
            });
        }
        @JavascriptInterface public String readText(String value) {
            try {
                ByteArrayOutputStream out = readUri(Uri.parse(value), 2 * 1024 * 1024);
                return new String(out.toByteArray(), StandardCharsets.UTF_8);
            } catch (Exception e) { return ""; }
        }
        @JavascriptInterface public String readDataUrl(String value) {
            try {
                Uri uri = Uri.parse(value);
                ByteArrayOutputStream out = readUri(uri, 32 * 1024 * 1024);
                String type = getContentResolver().getType(uri);
                if (type == null) type = "application/octet-stream";
                return "data:" + type + ";base64," + Base64.encodeToString(out.toByteArray(), Base64.NO_WRAP);
            } catch (Exception e) { return ""; }
        }
        @JavascriptInterface public String cacheIntroVideo(String value) {
            File target = new File(getCacheDir(), "karaoke-intro.mp4");
            try (InputStream in = getContentResolver().openInputStream(Uri.parse(value));
                 FileOutputStream out = new FileOutputStream(target, false)) {
                if (in == null) return "";
                byte[] buffer = new byte[65536];
                int read;
                long total = 0;
                while ((read = in.read(buffer)) != -1) {
                    total += read;
                    if (total > 1024L * 1024L * 1024L) return "";
                    out.write(buffer, 0, read);
                }
                out.flush();
                return Uri.fromFile(target).toString();
            } catch (Exception e) { return ""; }
        }
    }

    private void hideFullscreenView() {
        if (fullscreenView == null) return;
        if (fullscreenView.getParent() instanceof ViewGroup) {
            ((ViewGroup) fullscreenView.getParent()).removeView(fullscreenView);
        }
        fullscreenView = null;
        if (fullscreenCallback != null) fullscreenCallback.onCustomViewHidden();
        fullscreenCallback = null;
        enterImmersive();
    }

    private void enterImmersive() {
        getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY | View.SYSTEM_UI_FLAG_FULLSCREEN |
            View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN |
            View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_LAYOUT_STABLE);
    }

    @Override protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == PICK_FOLDER) {
            if (resultCode == RESULT_OK && data != null && data.getData() != null) loadDocumentTree(data.getData(), data.getFlags());
            return;
        }
        if (requestCode != PICK_FILES || fileCallback == null) return;
        Uri[] results = null;
        if (resultCode == RESULT_OK && data != null) {
            if (data.getClipData() != null) {
                int count = data.getClipData().getItemCount();
                results = new Uri[count];
                for (int i = 0; i < count; i++) results[i] = data.getClipData().getItemAt(i).getUri();
            } else if (data.getData() != null) results = new Uri[]{data.getData()};
        }
        fileCallback.onReceiveValue(results);
        fileCallback = null;
    }

    private ByteArrayOutputStream readUri(Uri uri, int limit) throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        try (InputStream in = getContentResolver().openInputStream(uri)) {
            if (in == null) return out;
            byte[] buffer = new byte[32768]; int read; int total = 0;
            while ((read = in.read(buffer)) != -1) {
                total += read; if (total > limit) throw new IllegalArgumentException("Arquivo grande demais para leitura em memória");
                out.write(buffer, 0, read);
            }
        }
        return out;
    }

    private void loadDocumentTree(Uri treeUri, int flags) {
        int grants = flags & (Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
        try { getContentResolver().takePersistableUriPermission(treeUri, grants & Intent.FLAG_GRANT_READ_URI_PERMISSION); }
        catch (Exception ignored) {}
        new Thread(new Runnable() {
            @Override public void run() {
                final JSONArray files = new JSONArray();
                try {
                    String rootId = DocumentsContract.getTreeDocumentId(treeUri);
                    String rootName = getDocumentName(treeUri, rootId);
                    notifyRootIntro(treeUri, rootId);
                    collectDocuments(treeUri, rootId, rootName, files);
                    final String json = files.toString();
                    runOnUiThread(new Runnable() {
                        @Override public void run() {
                            if (webView != null) webView.evaluateJavascript("window.onNativeFolderLoaded && window.onNativeFolderLoaded(" + json + ")", null);
                        }
                    });
                } catch (Exception e) {
                    runOnUiThread(new Runnable() {
                        @Override public void run() {
                            if (webView != null) webView.evaluateJavascript("window.onNativeFolderLoadFailed && window.onNativeFolderLoadFailed()", null);
                            Toast.makeText(MainActivity.this, "Não foi possível ler esta pasta. Tente outra unidade.", Toast.LENGTH_LONG).show();
                        }
                    });
                }
            }
        }, "karaoke-folder-scan").start();
    }

    private void notifyRootIntro(Uri treeUri, String rootId) {
        Uri children = DocumentsContract.buildChildDocumentsUriUsingTree(treeUri, rootId);
        try (Cursor cursor = getContentResolver().query(children,
                new String[]{Document.COLUMN_DOCUMENT_ID, Document.COLUMN_DISPLAY_NAME, Document.COLUMN_MIME_TYPE}, null, null, null)) {
            if (cursor == null) return;
            while (cursor.moveToNext()) {
                String id = cursor.getString(0);
                String name = cursor.getString(1);
                String mime = cursor.getString(2);
                if (name == null || !"intro.mp4".equalsIgnoreCase(name) || Document.MIME_TYPE_DIR.equals(mime)) continue;
                final String introUri = DocumentsContract.buildDocumentUriUsingTree(treeUri, id).toString();
                runOnUiThread(new Runnable() {
                    @Override public void run() {
                        if (webView != null) webView.evaluateJavascript(
                            "window.onIntroFoundDuringScan && window.onIntroFoundDuringScan(" + JSONObject.quote(introUri) + ")", null);
                    }
                });
                return;
            }
        } catch (Exception ignored) {}
    }

    private String getDocumentName(Uri treeUri, String documentId) {
        Uri document = DocumentsContract.buildDocumentUriUsingTree(treeUri, documentId);
        try (Cursor cursor = getContentResolver().query(document, new String[]{Document.COLUMN_DISPLAY_NAME}, null, null, null)) {
            if (cursor != null && cursor.moveToFirst()) return cursor.getString(0);
        } catch (Exception ignored) {}
        return "KARAOKE";
    }

    private void collectDocuments(Uri treeUri, String parentId, String parentPath, JSONArray files) throws Exception {
        Uri children = DocumentsContract.buildChildDocumentsUriUsingTree(treeUri, parentId);
        try (Cursor cursor = getContentResolver().query(children,
                new String[]{Document.COLUMN_DOCUMENT_ID, Document.COLUMN_DISPLAY_NAME, Document.COLUMN_MIME_TYPE}, null, null, null)) {
            if (cursor == null) return;
            while (cursor.moveToNext()) {
                String id = cursor.getString(0);
                String name = cursor.getString(1);
                String mime = cursor.getString(2);
                if (name == null || name.startsWith(".")) continue;
                String path = parentPath.isEmpty() ? name : parentPath + "/" + name;
                if (Document.MIME_TYPE_DIR.equals(mime)) {
                    collectDocuments(treeUri, id, path, files);
                } else {
                    JSONObject item = new JSONObject();
                    item.put("name", name);
                    item.put("path", path);
                    item.put("uri", DocumentsContract.buildDocumentUriUsingTree(treeUri, id).toString());
                    files.put(item);
                }
            }
        }
    }

    @Override public boolean dispatchKeyEvent(KeyEvent event) {
        if (event.getKeyCode() == KeyEvent.KEYCODE_BACK && rockDoidoActive) return true;
        if (event.getKeyCode() == KeyEvent.KEYCODE_BACK && event.getAction() == KeyEvent.ACTION_UP) {
            if (webView != null && webView.canGoBack()) webView.goBack(); else finish();
            return true;
        }
        return super.dispatchKeyEvent(event);
    }
    @Override public void onBackPressed() { if (rockDoidoActive) return; super.onBackPressed(); }
    @Override public void onWindowFocusChanged(boolean hasFocus) { super.onWindowFocusChanged(hasFocus); if (hasFocus) enterImmersive(); }
    @Override protected void onSaveInstanceState(Bundle out) { if (webView != null) webView.saveState(out); super.onSaveInstanceState(out); }
    @Override protected void onDestroy() { if (fileCallback != null) fileCallback.onReceiveValue(null); if (fullscreenView != null) hideFullscreenView(); if (webView != null) { webView.destroy(); webView = null; } super.onDestroy(); }
}
