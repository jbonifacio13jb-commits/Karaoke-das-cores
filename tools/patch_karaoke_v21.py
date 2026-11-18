#!/usr/bin/env python3
"""Ajustes seguros v2.1 do Karaokê das Cores.
Executado após o patch legado do workflow, tanto na cópia da raiz quanto
nos arquivos Android extraídos dos ZIPs de fonte.
"""
from pathlib import Path
import re

MARKER = "KARAOKE_CORES_PATCH_V21"

def replace_all(text, old, new, label):
    if old not in text:
        print("[AVISO] trecho não localizado:", label)
        return text
    print("[OK] aplicado:", label)
    return text.replace(old, new)

def patch_html(path: Path):
    text = path.read_text(encoding="utf-8")
    visual_changed = False
    if "KARAOKE_VISUAL_HOME_V23" not in text:
        home_markup = '''        <header id="home-brand-header">
            <div id="home-brand-lockup"><span id="home-mic" aria-hidden="true">🎤</span><div id="home-brand-title">KARAOKÊ<em>FESTA DAS CORES</em></div></div>
            <div id="home-tagline">Cante, Divirta-se<br>e Faça a Festa!</div>
            <button id="home-exit" type="button" onclick="sairAplicativoDaTelaInicial()">⇥ Sair</button>
        </header>
        <div class="stage" id="stage-area">'''
        home_css = '''<style id="KARAOKE_VISUAL_HOME_V23">
:root{--home-gold:#ffd329;--home-violet:#9200ff;--home-pink:#ff22cf;--home-night:#05031a}
html,body{width:100%;height:100%;background:var(--home-night)!important}
#ui-wrapper{display:grid!important;position:relative!important;isolation:isolate;grid-template-columns:minmax(0,1.94fr) minmax(300px,1fr)!important;grid-template-rows:minmax(88px,18vh) minmax(0,1fr) minmax(78px,13vh)!important;gap:1.35vh 1.15vw!important;padding:1.35vh 1.5vw!important;width:100vw!important;height:100vh!important;overflow:hidden;background:radial-gradient(ellipse at 18% 0%,rgba(129,0,255,.24),transparent 45%),radial-gradient(ellipse at 90% 100%,rgba(255,0,180,.18),transparent 42%),linear-gradient(145deg,#07051d,#02020d 75%)!important}
#home-brand-header{grid-column:1/3;grid-row:1;display:flex;align-items:center;justify-content:space-between;min-width:0;padding:0 1.2vw;position:relative;overflow:hidden;border-bottom:.28vh solid transparent;border-image:linear-gradient(90deg,#ffb800,#ff32d6,#7d35ff,#ffb800) 1;background:linear-gradient(90deg,rgba(15,5,38,.35),rgba(5,3,22,.06))}
#home-brand-lockup{display:flex;align-items:center;gap:1.2vw;min-width:0}
#home-mic{font-size:clamp(42px,8vh,100px);line-height:1;filter:drop-shadow(0 0 1.2vh #ff9d00) drop-shadow(0 0 1.6vh #c000ff)}
#home-brand-title{font:900 clamp(28px,6.1vh,76px)/.94 'Arial Black',Arial,sans-serif;letter-spacing:.015em;color:#ffd35b;text-shadow:0 .25vh .2vh #5b2600,0 0 1.4vh #ff9800}
#home-brand-title em{display:block;font-style:italic;font-size:.67em;letter-spacing:.025em;color:#ed45ff;text-shadow:0 0 1.2vh #9c00ff}
#home-tagline{margin-left:auto;margin-right:2vw;text-align:center;color:#ffd44d;font:italic 700 clamp(16px,3vh,38px)/1.08 cursive;transform:rotate(-3deg);text-shadow:0 0 1vh #ff8a00}
#home-exit{flex:0 0 auto;border:.22vh solid #bd63ff;border-radius:1.4vh;padding:1.1vh 1.8vw;background:linear-gradient(135deg,#30105a,#100625);color:#fff;font:800 clamp(14px,2.2vh,25px) Arial,sans-serif;box-shadow:0 0 1.5vh #a000ff;cursor:pointer}
#home-exit:focus{outline:.35vh solid var(--home-gold);transform:scale(1.06)}
.stage{grid-column:1;grid-row:2;position:relative!important;inset:auto!important;width:100%!important;height:100%!important;min-height:0!important;border:.28vh solid #a000ff!important;border-radius:1.8vh!important;overflow:hidden;box-shadow:0 0 1.6vh rgba(190,0,255,.65),inset 0 0 1.4vh rgba(255,30,220,.18)!important;background:#09031d!important}
.stage::after{content:"";position:absolute;inset:0;pointer-events:none;border:.18vh solid rgba(255,207,52,.75);border-radius:1.5vh;z-index:1200}
.stage-background{background-size:cover!important;background-position:center!important;opacity:.92!important}
#idle-hero{background:radial-gradient(ellipse at center,rgba(15,3,40,.12),rgba(5,0,20,.28))!important}
#idle-hero .hero-sub{color:#ffd52f!important}
#idle-hero .hero-titulo{font-size:clamp(26px,6vh,76px)!important;text-shadow:0 0 1.4vh #b000ff!important}
#idle-hero .hero-titulo em{background:linear-gradient(90deg,#fff1a5,#ffc52e,#ff40d4)!important;-webkit-background-clip:text!important;background-clip:text!important}
#idle-hero .hero-cta{background:linear-gradient(90deg,#ffdb35,#ff9d00)!important;color:#170b00!important}
.ui-panel{grid-column:2;grid-row:2;position:relative!important;min-width:0!important;min-height:0!important;display:flex!important;flex-direction:column!important;gap:1vh!important;padding:1.3vh 1vw!important;border:.25vh solid #9b18ff!important;border-radius:1.8vh!important;background:linear-gradient(160deg,rgba(24,5,55,.97),rgba(5,2,23,.97))!important;box-shadow:0 0 1.6vh rgba(180,0,255,.48),inset 0 0 1.4vh rgba(255,40,220,.08)!important}
.ui-panel::before{display:none!important}
.panel-head{order:0!important;flex:0 0 auto!important;min-height:5vh!important;padding:.4vh .5vw 1vh!important;border-bottom:.18vh solid #a000ff!important}
.ph-titulo{font:900 clamp(16px,2.6vh,32px) 'Arial Black',Arial,sans-serif!important;color:#ffe11d!important;letter-spacing:.02em!important}
.ph-titulo small{display:none!important}
.ph-count{background:linear-gradient(135deg,#a000ff,#ed27ca)!important;color:#fff!important;border-radius:1vh!important}
#track-list{order:1!important;flex:1!important;min-height:0!important;overflow-y:auto!important;display:flex!important;flex-direction:column!important;gap:.7vh!important;padding:.6vh .35vw!important;background:rgba(5,1,20,.92)!important;border:0!important;border-radius:0 0 1vh 1vh!important}
#track-list:empty::before{content:'A fila está vazia\A Escolha uma música pelo código ou catálogo'!important;color:#d8c8ff!important;font:700 clamp(13px,2vh,22px)/1.5 Arial,sans-serif!important}
.item{display:flex!important;align-items:center!important;gap:.7vw!important;min-height:0!important;flex-shrink:0!important;padding:.75vh .55vw!important;margin:0!important;border-radius:.8vh!important;border:0!important;border-bottom:.14vh solid rgba(172,35,255,.8)!important;border-left:.35vw solid #c000ff!important;background:linear-gradient(90deg,rgba(95,20,145,.3),rgba(20,5,45,.25))!important}
.item.now-playing{border-left-color:#ffe02d!important;background:linear-gradient(90deg,rgba(255,196,0,.24),rgba(70,10,90,.2))!important}
.it-pos{flex:0 0 3.8vh!important;width:3.8vh!important;height:3.8vh!important;border-radius:.65vh!important;background:#220d50!important;color:#ffe22a!important;font:900 clamp(13px,2vh,24px) Arial,sans-serif!important}
.it-titulo{font:800 clamp(13px,2vh,24px)/1.1 Arial,sans-serif!important;color:#fff!important}
.it-cantor{font:500 clamp(11px,1.65vh,20px) Arial,sans-serif!important;color:#d9c8ff!important;letter-spacing:0!important}
.it-codigo{font:800 clamp(11px,1.55vh,19px) Arial,sans-serif!important;color:#ffe21b!important;background:transparent!important;border:0!important;padding:0!important}
.playing-badge{font-size:clamp(8px,1.1vh,13px)!important}
.controls-grid{order:2!important;display:flex!important;flex:0 0 auto!important;gap:.6vw!important;padding:.4vh 0 0!important}
.controls-grid button{min-height:3.8vh!important;padding:.55vh .7vw!important;border-radius:.7vh!important;font:800 clamp(10px,1.45vh,17px) Arial,sans-serif!important}
.search-bar{grid-column:1;grid-row:3;position:relative!important;left:auto!important;right:auto!important;bottom:auto!important;width:100%!important;height:100%!important;min-height:0!important;display:flex!important;align-items:stretch!important;gap:1.1vw!important;padding:0!important;margin:0!important;background:transparent!important;border:0!important}
#btn-teclado,#btn-catalogo,#btn-play-bar{flex:1 1 0!important;min-width:0!important;width:auto!important;height:100%!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:.8vw!important;padding:0 1vw!important;border-radius:1.8vh!important;color:#fff!important;font:900 clamp(14px,2.7vh,34px) 'Arial Black',Arial,sans-serif!important;letter-spacing:.025em!important;text-shadow:0 .15vh .3vh #000!important;border:.25vh solid #ff42dc!important;box-shadow:inset 0 .25vh .4vh rgba(255,255,255,.35),0 .55vh 0 rgba(25,0,55,.9),0 0 1.5vh rgba(190,0,255,.6)!important}
#btn-teclado,#btn-catalogo{background:linear-gradient(145deg,#8e00e9,#390071 70%,#16002f)!important}
#btn-teclado svg,#btn-catalogo svg{width:4.5vh!important;height:4.5vh!important;fill:none!important;stroke:#fff!important;stroke-width:2!important}
#btn-play-bar{flex:1.15 1 0!important;background:linear-gradient(180deg,#fff47a,#ffc400 48%,#ff9200)!important;color:#170900!important;text-shadow:0 .12vh .1vh rgba(255,255,255,.6)!important;border-color:#fff2a1!important;box-shadow:inset 0 .3vh .5vh #fff,0 .55vh 0 #8b4200,0 0 2vh #ffad00!important}
#btn-play-bar:disabled{filter:grayscale(.5) brightness(.72)!important;opacity:.8!important}
#btn-teclado:focus,#btn-catalogo:focus,#btn-play-bar:focus{outline:.35vh solid #fff!important;transform:translateY(-.3vh) scale(1.025)!important}
#tv-code-display{z-index:100!important}
#marca-agua{display:none!important}
#home-brand-header,#home-exit{z-index:30}
@media(max-aspect-ratio:4/3){#ui-wrapper{grid-template-columns:minmax(0,1fr)!important;grid-template-rows:12vh minmax(28vh,.85fr) minmax(20vh,1fr) 10vh!important;overflow:auto!important}#home-brand-header{grid-column:1;grid-row:1}.stage{grid-column:1;grid-row:2}.ui-panel{grid-column:1;grid-row:3}.search-bar{grid-column:1;grid-row:4}#home-tagline{display:none}}
</style>'''
        text = text.replace('        <div class="stage" id="stage-area">', home_markup, 1)
        text = text.replace("</head>", home_css + "\n</head>", 1)
        text = text.replace("        function logOK(msg)", "        function sairAplicativoDaTelaInicial() { try { if (window.AndroidHost && AndroidHost.exitApp) { AndroidHost.exitApp(); return; } } catch (_) {} try { window.close(); } catch (_) {} }\n        function logOK(msg)", 1)
        visual_changed = True
    if "KARAOKE_STARTUP_GATE_V24" not in text:
        # Impede que o palco apareça antes da permissão e da leitura da pasta.
        boot = "        let folderLoadFinished = true; var ui = document.getElementById('ui-wrapper'); if (ui && (!document.getElementById('intro-video') || !document.getElementById('intro-video').src || document.getElementById('intro-video').paused)) { ui.classList.remove('oculto-inicio'); ui.classList.add('liberado'); ui.style.display = ''; ui.style.opacity = ''; ui.style.visibility = ''; if (typeof aplicarLayoutFestaDasCores === 'function') aplicarLayoutFestaDasCores(); }"
        text = text.replace(boot, "        let folderLoadFinished = true;", 1)
        # A intro não pode tocar automaticamente enquanto o Android ainda lê a pasta.
        text = text.replace("introVideo.autoplay = true;", "introVideo.autoplay = false;")
        text = text.replace("            introVideo.muted = false;\n            try {\n                await forcarPaisagem();", "            introVideo.muted = true;\n            introVideo.volume = 1;\n            try {\n                await forcarPaisagem();", 1)
        frame_old = "                    if (introVideo.requestVideoFrameCallback) {\n                        await new Promise(resolve => introVideo.requestVideoFrameCallback(resolve));\n                    }\n                    introCurtain.classList.add('hidden');"
        frame_new = "                    if (introVideo.requestVideoFrameCallback) {\n                        await new Promise(resolve => introVideo.requestVideoFrameCallback(resolve));\n                    } else {\n                        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));\n                    }\n                    introCurtain.classList.add('hidden');\n                    introVideo.muted = false;"
        text = text.replace(frame_old, frame_new, 1)
        # Aguarda a montagem do catálogo antes de iniciar a intro.
        text = text.replace("                const introPlayback = intro ? iniciarIntroDuranteCarregamento() : null;\n                await handleFolderSelect({ target: { files } });", "                await handleFolderSelect({ target: { files } });\n                const introPlayback = intro ? iniciarIntroDuranteCarregamento() : null;", 1)
        # handleFolderSelect termina a leitura, mas não revela o palco por conta própria.
        unlock_old = "            folderLoadFinished = true; var ui = document.getElementById('ui-wrapper'); if (ui && (!document.getElementById('intro-video') || !document.getElementById('intro-video').src || document.getElementById('intro-video').paused)) { ui.classList.remove('oculto-inicio'); ui.classList.add('liberado'); ui.style.display = ''; ui.style.opacity = ''; ui.style.visibility = ''; if (typeof aplicarLayoutFestaDasCores === 'function') aplicarLayoutFestaDasCores(); }"
        text = text.replace(unlock_old, "            folderLoadFinished = true;", 1)
        fail_old = "        window.onNativeFolderLoadFailed = function() {\n            folderLoadFinished = true; var ui = document.getElementById('ui-wrapper'); if (ui && (!document.getElementById('intro-video') || !document.getElementById('intro-video').src || document.getElementById('intro-video').paused)) { ui.classList.remove('oculto-inicio'); ui.classList.add('liberado'); ui.style.display = ''; ui.style.opacity = ''; ui.style.visibility = ''; if (typeof aplicarLayoutFestaDasCores === 'function') aplicarLayoutFestaDasCores(); }\n        };"
        fail_new = "        window.onNativeFolderLoadFailed = function() {\n            folderLoadFinished = true;\n            exibirErroIntro('Não foi possível carregar a pasta autorizada. Escolha a pasta novamente.', true);\n        };"
        text = text.replace(fail_old, fail_new, 1)
        helper = "        function liberarInterfaceAposCarga() { const ui = document.getElementById('ui-wrapper'); if (!ui) return; ui.classList.remove('oculto-inicio'); ui.classList.add('liberado'); ui.style.display = ''; ui.style.opacity = ''; ui.style.visibility = ''; if (typeof aplicarLayoutFestaDasCores === 'function') aplicarLayoutFestaDasCores(); }\n"
        text = text.replace("        function exibirErroIntro(mensagem, selecionarPasta) {", helper + "        function exibirErroIntro(mensagem, selecionarPasta) {", 1)
        text = text.replace("                    logAviso('Pasta autorizada, mas não encontrei slides nem intro.mp4/intro2.mp4. Use Selecionar pasta para tentar outra pasta.');", "                    liberarInterfaceAposCarga();\n                    logAviso('Pasta autorizada, mas não encontrei slides nem intro.mp4/intro2.mp4. Use Selecionar pasta para tentar outra pasta.');", 1)
        text = text.replace("<!-- KARAOKE_STARTUP_GATE_V22 -->", "<!-- KARAOKE_STARTUP_GATE_V22 -->", 1)
        text = text.replace("</body>", "\n<!-- KARAOKE_STARTUP_GATE_V24 -->\n</body>", 1)
        visual_changed = True
    if MARKER in text and "KARAOKE_STARTUP_GATE_V22" in text:
        if visual_changed:
            path.write_text(text, encoding="utf-8")
        return
    # Corrige a inicialização: a interface permanece oculta até a pasta estar
    # autorizada e a intro ter exibido o primeiro quadro; o áudio só entra depois.
    STARTUP_MARKER = "KARAOKE_STARTUP_GATE_V22"
    if STARTUP_MARKER not in text:
        old_boot = "        let folderLoadFinished = true; var ui = document.getElementById('ui-wrapper'); if (ui && (!document.getElementById('intro-video') || !document.getElementById('intro-video').src || document.getElementById('intro-video').paused)) { ui.classList.remove('oculto-inicio'); ui.classList.add('liberado'); ui.style.display = ''; ui.style.opacity = ''; ui.style.visibility = ''; if (typeof aplicarLayoutFestaDasCores === 'function') aplicarLayoutFestaDasCores(); }"
        text = text.replace(old_boot, "        let folderLoadFinished = true;", 1)

        # Não deixar o elemento de vídeo iniciar sozinho durante a varredura SAF.
        text = text.replace("introVideo.autoplay = true;", "introVideo.autoplay = false;")

        # Primeiro termina a leitura da pasta/catálogo; só então começa a sequência.
        old_order = "                const introPlayback = intro ? iniciarIntroDuranteCarregamento() : null;\n                await handleFolderSelect({ target: { files } });"
        new_order = "                await handleFolderSelect({ target: { files } });\n                const introPlayback = intro ? iniciarIntroDuranteCarregamento() : null;"
        text = text.replace(old_order, new_order, 1)

        # Sem intro, libera a tela somente depois da leitura completa da pasta.
        old_no_intro = "                    logAviso('Pasta autorizada, mas não encontrei slides nem intro.mp4/intro2.mp4. Use Selecionar pasta para tentar outra pasta.');"
        new_no_intro = "                    if (typeof liberarInterfaceAposCarga === 'function') liberarInterfaceAposCarga();\n" + old_no_intro
        text = text.replace(old_no_intro, new_no_intro, 1)

        # Não liberar o palco por estar simplesmente pausado/sem src.
        old_final_unlock = "            folderLoadFinished = true; var ui = document.getElementById('ui-wrapper'); if (ui && (!document.getElementById('intro-video') || !document.getElementById('intro-video').src || document.getElementById('intro-video').paused)) { ui.classList.remove('oculto-inicio'); ui.classList.add('liberado'); ui.style.display = ''; ui.style.opacity = ''; ui.style.visibility = ''; if (typeof aplicarLayoutFestaDasCores === 'function') aplicarLayoutFestaDasCores(); }"
        text = text.replace(old_final_unlock, "            folderLoadFinished = true;", 1)

        old_fail = "        window.onNativeFolderLoadFailed = function() {\n            folderLoadFinished = true; var ui = document.getElementById('ui-wrapper'); if (ui && (!document.getElementById('intro-video') || !document.getElementById('intro-video').src || document.getElementById('intro-video').paused)) { ui.classList.remove('oculto-inicio'); ui.classList.add('liberado'); ui.style.display = ''; ui.style.opacity = ''; ui.style.visibility = ''; if (typeof aplicarLayoutFestaDasCores === 'function') aplicarLayoutFestaDasCores(); }\n        };"
        new_fail = "        window.onNativeFolderLoadFailed = function() {\n            folderLoadFinished = true;\n            if (typeof exibirErroIntro === 'function') exibirErroIntro('Não foi possível carregar a pasta autorizada. Escolha a pasta novamente.', true);\n        };"
        text = text.replace(old_fail, new_fail, 1)

        # A intro fica muda durante o carregamento e só libera som após o primeiro quadro.
        old_mute = "            introVideo.muted = false;\n            try {\n                await forcarPaisagem();"
        new_mute = "            introVideo.muted = true;\n            introVideo.volume = 1;\n            try {\n                await forcarPaisagem();"
        text = text.replace(old_mute, new_mute, 1)

        old_frame = "                    if (introVideo.requestVideoFrameCallback) {\n                        await new Promise(resolve => introVideo.requestVideoFrameCallback(resolve));\n                    }\n                    introCurtain.classList.add('hidden');"
        new_frame = "                    if (introVideo.requestVideoFrameCallback) {\n                        await new Promise(resolve => introVideo.requestVideoFrameCallback(resolve));\n                    } else {\n                        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));\n                    }\n                    introCurtain.classList.add('hidden');\n                    introVideo.muted = false;"
        text = text.replace(old_frame, new_frame, 1)

        text = text.replace("        function exibirErroIntro(", "        function liberarInterfaceAposCarga() {\n            const ui = document.getElementById('ui-wrapper');\n            if (!ui) return;\n            ui.classList.remove('oculto-inicio');\n            ui.classList.add('liberado');\n            ui.style.display = '';\n            ui.style.opacity = '';\n            ui.style.visibility = '';\n            if (typeof aplicarLayoutFestaDasCores === 'function') aplicarLayoutFestaDasCores();\n        }\n        window.liberarInterfaceAposCarga = liberarInterfaceAposCarga;\n\n        function exibirErroIntro(", 1)

        text = text.replace("</body>", "\n<!-- " + STARTUP_MARKER + " -->\n</body>", 1)

    if MARKER in text:
        path.write_text(text, encoding="utf-8")
        print("[OK] HTML atualizado: inicialização sem tela preta", path)
        return

    # Cinco intros em ordem, mantendo intr2.mp4 como nome legado alternativo.
    helper = r"""
        function ordemArquivoIntro(nome) {
            const n = String(nome || '').toLowerCase();
            if (n === 'intro.mp4') return 0;
            const m = n.match(/^intro([1-5])\.mp4$/);
            if (m) return Number(m[1]);
            if (n === 'intr2.mp4') return 2;
            return 99;
        }
"""
    text = replace_all(text, "        async function reproduzirSequenciaIntro() {",
                       helper + "\n        async function reproduzirSequenciaIntro() {",
                       "ordenação das cinco intros")

    old_filter = r"const introFiles = (entries || []).filter(item => /^(?:intro2?|intr2)\.mp4$/i.test(item.name || '')).sort((a, b) => (/^intro\.mp4$/i.test(a.name) ? 0 : 1) - (/^intro\.mp4$/i.test(b.name) ? 0 : 1));"
    new_filter = r"const introFiles = (entries || []).filter(item => /^(?:intro(?:[1-5])?|intr2)\.mp4$/i.test(item.name || '')).sort((a, b) => ordemArquivoIntro(a.name) - ordemArquivoIntro(b.name));"
    text = replace_all(text, old_filter, new_filter, "detecção das intros na pasta SAF")

    old_map_native = r"introSequenceFiles = introFiles.map(item => ({ file: item, name: item.name, order: /^intro\.mp4$/i.test(item.name) ? 0 : 1 }));"
    new_map_native = r"introSequenceFiles = introFiles.map(item => ({ file: item, name: item.name, order: ordemArquivoIntro(item.name) }));"
    text = replace_all(text, old_map_native, new_map_native, "ordem das intros SAF")

    old_filter_local = r"const introFiles = files.filter(f => /^(?:intro2?|intr2)\.mp4$/i.test(f.name || '')).sort((a, b) => (/^intro\.mp4$/i.test(a.name) ? 0 : 1) - (/^intro\.mp4$/i.test(b.name) ? 0 : 1));"
    new_filter_local = r"const introFiles = files.filter(f => /^(?:intro(?:[1-5])?|intr2)\.mp4$/i.test(f.name || '')).sort((a, b) => ordemArquivoIntro(a.name) - ordemArquivoIntro(b.name));"
    text = replace_all(text, old_filter_local, new_filter_local, "detecção das intros no seletor web")

    old_map_local = r"introSequenceFiles = introFiles.map(file => ({ file, name: file.name, order: /^intro\.mp4$/i.test(file.name) ? 0 : 1 }));"
    new_map_local = r"introSequenceFiles = introFiles.map(file => ({ file, name: file.name, order: ordemArquivoIntro(file.name) }));"
    text = replace_all(text, old_map_local, new_map_local, "ordem das intros no seletor web")

    # Intro e vídeos da pasta RockDoido nunca entram no catálogo de músicas.
    old_catalog = r"const mp4s = files.filter(f => /\.mp4$/i.test(f.name || '') && (f.name || '').toLowerCase() !== 'intro.mp4');"
    new_catalog = r"const mp4s = files.filter(f => /\.mp4$/i.test(f.name || '') && !/^(?:intro(?:[1-5])?|intr2)\.mp4$/i.test(f.name || '') && !/(?:^|\/)(?:ROCK ?DOIDO|MODO ROCKDOIDO)(?:\/|$)/i.test(f.webkitRelativePath || ''));"
    text = replace_all(text, old_catalog, new_catalog, "exclusão de intros e vídeos RockDoido do catálogo")

    text = text.replace("Confira intro.mp4 e intro2.mp4.", "Confira intro.mp4, intro2.mp4, intro3.mp4, intro4.mp4 e intro5.mp4.")
    text = text.replace("Não encontrei intro.mp4 nem intro2.mp4 na pasta escolhida.", "Não encontrei os vídeos intro.mp4 até intro5.mp4 na pasta escolhida.")
    text = text.replace("intro.mp4/intro2.mp4 não encontrados", "intro.mp4 até intro5.mp4 não encontrados")
    text = text.replace("Não encontrei intro.mp4 nem intro2.mp4 na pasta escolhida. Selecione", "Não encontrei intro.mp4 até intro5.mp4 na pasta escolhida. Selecione")

    # Adia a leitura do MP3 até o momento da reprodução, evitando Base64 na varredura.
    old_eager_audio = """                        let audioSrc = f.contentUri || URL.createObjectURL(f);
                        if (f.contentUri && window.AndroidHost && AndroidHost.readDataUrl) {
                            try {
                                const inlineAudio = AndroidHost.readDataUrl(f.contentUri);
                                if (inlineAudio && inlineAudio.startsWith('data:audio/')) audioSrc = inlineAudio;
                            } catch (err) { logAviso('O MP3 será aberto pelo endereço da pasta selecionada.'); }
                        }
"""
    new_lazy_audio = """                        // A leitura nativa do MP3 só ocorre como fallback ao iniciar o áudio.
                        let audioSrc = f.contentUri || URL.createObjectURL(f);
"""
    text = replace_all(text, old_eager_audio, new_lazy_audio, "carregamento sob demanda do MP3 RockDoido")

    # Captura um MP4 dentro da pasta RockDoido para reprodução em vídeo.
    text = replace_all(text,
        "let videoFiles = {}, catalog = [], queue = [], rockDoidoSlides = [], bgCantores = {}, exitTimer, slideInterval;",
        "let videoFiles = {}, catalog = [], queue = [], rockDoidoSlides = [], bgCantores = {}, exitTimer, slideInterval;\n        let _videoRockDoido = null;",
        "variável de vídeo RockDoido")

    text = replace_all(text,
        "videoFiles = {}; rockDoidoSlides = []; bgCantores = {}; catalog = [];",
        "videoFiles = {}; rockDoidoSlides = []; bgCantores = {}; catalog = []; _videoRockDoido = null;",
        "reinicialização do vídeo RockDoido ao trocar pasta")

    old_rock = "const emRockdoido = path.includes('ROCKDOIDO') || path.includes('ROCK DOIDO') || \n                                    path.includes('MODO ROCKDOIDO');"
    new_rock = "const emRockdoido = path.includes('ROCKDOIDO') || path.includes('ROCK DOIDO') || \n                                    path.includes('MODO ROCKDOIDO');\n                if (emRockdoido && name.endsWith('.MP4') && !_videoRockDoido) _videoRockDoido = f;"
    text = replace_all(text, old_rock, new_rock, "identificação do MP4 RockDoido")

    text = replace_all(text, "                tocarAudioRockDoido();\n\n                startRockDoidoSync();",
                       "                if (!_videoRockDoido) tocarAudioRockDoido();\n\n                startRockDoidoSync();",
                       "prioridade do vídeo sobre o MP3 no RockDoido")

    # Reproduz o MP4 no palco RockDoido. Se a WebView não conseguir abrir o URI,
    # retorna automaticamente ao modo antigo de MP3 + slides.
    rock_insert = r"""
            if (_videoRockDoido) {
                const slideLayer = document.getElementById('bg-singer-layer-rock');
                if (slideLayer) { slideLayer.style.opacity = '0'; slideLayer.classList.remove('ativo'); }
                document.body.classList.remove('tem-slide');
                let rockVideo = document.getElementById('rockdoido-video');
                if (!rockVideo) {
                    rockVideo = document.createElement('video');
                    rockVideo.id = 'rockdoido-video';
                    rockVideo.setAttribute('playsinline', '');
                    rockVideo.setAttribute('webkit-playsinline', '');
                    rockVideo.setAttribute('preload', 'auto');
                    rockVideo.controls = false;
                    rockVideo.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1002;background:#000;display:none;';
                    tornadoLayer.appendChild(rockVideo);
                }
                const videoUrl = _videoRockDoido.contentUri || URL.createObjectURL(_videoRockDoido);
                rockVideo.pause();
                rockVideo.src = videoUrl;
                rockVideo.loop = true;
                rockVideo.muted = false;
                rockVideo.style.display = 'block';
                const tentativaVideo = rockVideo.play();
                if (tentativaVideo && typeof tentativaVideo.then === 'function') {
                    tentativaVideo.then(() => {
                        pararAudioRockDoido();
                        logOK('Vídeo do modo RockDoido em reprodução.');
                    }).catch(() => {
                        rockVideo.pause();
                        rockVideo.removeAttribute('src');
                        rockVideo.style.display = 'none';
                        _videoRockDoido = null;
                        logAviso('Este aparelho não conseguiu reproduzir o MP4 RockDoido. Voltando ao modo de áudio e slides.');
                        tocarAudioRockDoido();
                        startRockDoidoSync();
                    });
                }
                return;
            }
"""
    text = replace_all(text, "            logInfo('Slides disponíveis: ' + rockDoidoSlides.length);",
                       "            logInfo('Slides disponíveis: ' + rockDoidoSlides.length);\n" + rock_insert,
                       "reprodução opcional de vídeo RockDoido")

    text = replace_all(text, "                pararAudioRockDoido();\n\n                clearInterval(slideInterval);",
                       "                pararAudioRockDoido();\n                const rockVideo = document.getElementById('rockdoido-video');\n                if (rockVideo) { rockVideo.pause(); rockVideo.removeAttribute('src'); rockVideo.load(); rockVideo.style.display = 'none'; }\n\n                clearInterval(slideInterval);",
                       "encerramento do vídeo RockDoido")

    # Ordena fundo base + bgpadrao2..5; mantém nomes adicionais já existentes.
    old_bg = r"""if (bgPadraoGif) {
                bgPadraoList = [bgPadraoGif.contentUri || URL.createObjectURL(bgPadraoGif)];
                iniciarRotacaoBg();
            } else if (bgPadraoFiles.length > 0) {
                bgPadraoList = bgPadraoFiles.map(f => f.contentUri || URL.createObjectURL(f));
                iniciarRotacaoBg();
            }"""
    new_bg = r"""if (bgPadraoGif) bgPadraoFiles.unshift(bgPadraoGif);
            bgPadraoFiles.sort((a, b) => {
                const rank = f => {
                    const base = String(f.name || '').replace(/^bgpadr[ãa]o/i, '').replace(/\.[^.]+$/, '');
                    const n = base ? Number(base) : 0;
                    if (n === 0) return 0;
                    if (n >= 2 && n <= 5) return n - 1;
                    return 10 + (Number.isFinite(n) ? n : 99);
                };
                return rank(a) - rank(b) || String(a.name || '').localeCompare(String(b.name || ''), undefined, {numeric:true, sensitivity:'base'});
            });
            if (bgPadraoFiles.length > 0) {
                bgPadraoList = bgPadraoFiles.map(f => f.contentUri || URL.createObjectURL(f));
                iniciarRotacaoBg();
            }"""
    text = replace_all(text, old_bg, new_bg, "ordem dos fundos bgpadrao até bgpadrao5")

    # Corrige escrita do TXT: passa o URI exato da lista selecionada.
    text = replace_all(text,
        "try { gravou = !!AndroidHost.writeListaTxt(conteudo); } catch (_) { gravou = false; }",
        "try { gravou = !!AndroidHost.writeListaTxt(listas[0].contentUri, conteudo); } catch (_) { gravou = false; }",
        "gravação do lista.txt no arquivo selecionado")

    # O fundo padrão continua visível na contagem quando não existe foto do cantor.
    css_js = r"""
<style id="karaoke-cores-v21">
/* Palco realmente cheio: a fila e os controles laterais desaparecem e voltam ao sair. */
body.fullscreen-mode .search-bar,
body.fullscreen-mode .ui-panel {
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
}
body.fullscreen-mode .stage,
body.fullscreen-mode .stage-background {
    background-size: cover !important;
    background-position: center center !important;
}
body.countdown-ativo.countdown-sem-foto .stage-background {
    opacity: .78 !important;
    visibility: visible !important;
}
#rockdoido-video { object-fit: cover !important; }
#btn-sair-app-fixo, #btn-sair-topo-oficial, .btn-sair-topo-fixo, .btn-sair-transparente {
    position: fixed !important;
    top: 12px !important;
    right: 14px !important;
    left: auto !important;
    width: 36px !important;
    height: 36px !important;
    opacity: .56 !important;
    background: rgba(0,0,0,.22) !important;
    border: 1px solid rgba(255,255,255,.24) !important;
    box-shadow: none !important;
    z-index: 999999 !important;
}
#btn-sair-app-fixo:focus, #btn-sair-topo-oficial:focus,
.btn-sair-topo-fixo:focus, .btn-sair-transparente:focus {
    opacity: 1 !important;
    background: rgba(90,55,130,.72) !important;
    border-color: rgba(255,255,255,.7) !important;
}
</style>
<script id="karaoke-cores-v21-runtime">
(function () {
    if (window.__karaokeCoresV21Installed) return;
    window.__karaokeCoresV21Installed = true;

    function posicionarBotaoSair() {
        document.querySelectorAll('#btn-sair-app-fixo, #btn-sair-topo-oficial, .btn-sair-topo-fixo, .btn-sair-transparente').forEach(function (b) {
            b.style.position = 'fixed';
            b.style.top = '12px';
            b.style.right = '14px';
            b.style.left = 'auto';
            b.style.opacity = '.56';
        });
    }
    document.addEventListener('DOMContentLoaded', posicionarBotaoSair);
    window.addEventListener('load', posicionarBotaoSair);
    setTimeout(posicionarBotaoSair, 900);

    // Usa o fundo rotativo quando o cantor não possui foto própria.
    if (typeof window.startPlaylist === 'function') {
        const iniciarOriginal = window.startPlaylist;
        window.startPlaylist = async function () {
            let usarFundoPadrao = false;
            try {
                const atual = (typeof queue !== 'undefined' && queue.length) ? queue[0] : null;
                if (atual && document.body && !document.body.classList.contains('modo-jb')) {
                    const cantor = String(atual.singer || '').toUpperCase();
                    const chaves = cantor && cantor !== 'CONVIDADO' ? [cantor, cantor.charAt(0)] : [];
                    const temFoto = chaves.some(function (k) { return !!(bgCantores[k] || bgCantores[k + '2']); });
                    usarFundoPadrao = !temFoto && !_bgOficialUrl;
                    if (usarFundoPadrao) document.body.classList.add('countdown-sem-foto');
                }
            } catch (_) {}
            try { return await iniciarOriginal.apply(this, arguments); }
            finally { document.body.classList.remove('countdown-sem-foto'); }
        };
    }
})();
</script>
"""
    text = replace_all(text, "</body>", "\n" + MARKER + "\n" + css_js + "\n</body>", "estilos e fallback visual v2.1")

    path.write_text(text, encoding="utf-8")
    print("[OK] HTML atualizado:", path)

def patch_java(path: Path):
    text = path.read_text(encoding="utf-8")
    changed = False

    if "import java.io.OutputStream;" not in text:
        text = text.replace("import java.io.InputStream;", "import java.io.InputStream;\nimport java.io.OutputStream;")
        changed = True

    text = text.replace(
        "Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION",
        "Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION"
    )

    text = text.replace(
        "try { getContentResolver().takePersistableUriPermission(treeUri, grants & Intent.FLAG_GRANT_READ_URI_PERMISSION); }",
        "try { getContentResolver().takePersistableUriPermission(treeUri, grants); }"
    )

    # A sequência completa começa após a listagem SAF, evitando tocar intro.mp4 duas vezes.
    text = text.replace("                    notifyRootIntro(treeUri, rootId);",
                        "                    // Intros são iniciadas em ordem pelo JavaScript após a listagem completa.")

    # A leitura SAF envia ao JavaScript apenas tipos de arquivo usados pelo app.
    collect_anchor = """                } else {
                    JSONObject item = new JSONObject();
                    item.put("name", name);"""
    collect_replacement = """                } else {
                    String lowerName = name.toLowerCase(java.util.Locale.ROOT);
                    boolean relevant = lowerName.equals("lista.txt") || lowerName.equals("logo.png") ||
                        lowerName.equals("bgoficial.png") ||
                        lowerName.matches(".*\\\\.(mp4|mp3|jpg|jpeg|png|gif|webp|bmp|svg|avif)$");
                    if (!relevant) continue;
                    JSONObject item = new JSONObject();
                    item.put("name", name);"""
    if collect_anchor in text:
        text = text.replace(collect_anchor, collect_replacement, 1)
        changed = True

    if "writeListaTxt(String uriStr, String conteudo)" not in text:
        bridge = r"""
        @JavascriptInterface public boolean writeListaTxt(String uriStr, String conteudo) {
            try (OutputStream out = getContentResolver().openOutputStream(Uri.parse(uriStr), "wt")) {
                if (out == null) return false;
                out.write(conteudo.getBytes(StandardCharsets.UTF_8));
                out.flush();
                return true;
            } catch (Exception e) { return false; }
        }
"""
        text = text.replace("        @JavascriptInterface public String cacheIntroVideo(String value) {",
                            bridge + "\n        @JavascriptInterface public String cacheIntroVideo(String value) {")
        changed = True

    if text != path.read_text(encoding="utf-8"):
        changed = True
    if changed:
        path.write_text(text, encoding="utf-8")
        print("[OK] Java atualizado:", path)

def main():
    html_files = list(Path(".").rglob("index.html"))
    java_files = list(Path(".").rglob("MainActivity.java"))
    for path in html_files:
        patch_html(path)
    for path in java_files:
        patch_java(path)
    print(f"[RESUMO] {len(html_files)} HTML(s), {len(java_files)} MainActivity.java(s) verificados.")

if __name__ == "__main__":
    main()
