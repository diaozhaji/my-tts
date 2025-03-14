

import re
import unicodedata

def clean_text(text):
    """深度清洗文本的复合函数"""
    # 第一阶段：换行符规范化
    text = re.sub(r'\r\n|\r|\u2028|\u2029', '\n', text)  # 统一换行符
    text = re.sub(r'(?<![。！？…])[\n]+(?![，。！？])', ' ', text)  # 移除句中换行
    text = re.sub(r'\n{3,}', '\n\n', text)  # 保留最多两个连续换行

    # 第二阶段：字符过滤与转换
    allowed_chars = r'[\u4e00-\u9fa5a-zA-Z0-9，。！？；：“”‘’【】、（）《》—\-\s]'
    text = re.sub(f'[^{allowed_chars}]', '', text)
    
    # 第三阶段：标点标准化
    punct_map = str.maketrans({'，': ',', '。': '.', '；': ';', '：': ':', '‘': "'", '’': "'", 
                              '“': '"', '”': '"', '！': '!', '？': '?', '（': '(', '）': ')'})
    text = text.translate(punct_map)
    
    # 第四阶段：全角字符转换
    text = unicodedata.normalize('NFKC', text)  # 同时处理全角数字/字母
    
    # 第五阶段：空白规范化
    text = re.sub(r'[ \t\u3000]+', ' ', text)  # 合并多种空白符
    text = re.sub(r'\n +', '\n', text)  # 移除行首空格
    return text.strip()

def process_text(text):
    # 替换所有换行符为句号（保留段落停顿）
    text = re.sub(r'[\r\n]+', '', text)
    # 清理其他非法字符
    #text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。！？；：“”‘’—、（）《》\-\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

# 原始文本（包含需要清洗的内容）
text = """
   好的，用户需要开发一个Java工具，用来对比两次Maven构建生成的app.jar的差异，特别是要处理嵌套的JAR文件，并且需要确保只有真正有变化的class文件才被识别出来，而不仅仅是二进制差异。这需要我仔细思考如何设计和实现这样的工具。

首先，用户提到的app.jar可能是一个包含多个嵌套JAR的Fat JAR，比如使用maven-assembly-plugin或Spring Boot的打包方式生成的。这种情况下，直接对比整个JAR的二进制差异是没有意义的，因为时间戳或者无关的元数据变化也会导致差异，但用户关心的是实际的class内容变化。因此，需要递归解压所有嵌套的JAR，并逐层对比里面的class文件。

接下来，我需要确定如何高效地解压和遍历这些嵌套的JAR。Java自带的ZipInputStream可以处理，但可能需要处理多层嵌套，这需要考虑递归解压的策略。同时，处理大量文件时，性能也是一个问题，可能需要多线程或NIO来优化。

然后，关于如何判断class文件是否有实际变化。简单的做法是对每个class文件计算哈希值（如SHA-256），如果哈希值不同，则内容有变化。但用户强调二进制差异不算，可能需要进一步分析，比如反编译后比较源码，或者使用字节码分析工具如ASM来比较方法级别的差异。不过，考虑到工具的实现复杂度，先使用哈希值比较作为初步筛选，后续再考虑更深入的分析可能更实际。

另外，需要考虑排除一些无关的文件，比如时间戳变化的MANIFEST.MF，或者资源文件中的版本信息。用户可能只关心class文件的变动，所以需要过滤出.class文件进行重点比较。

工具的输出需要清晰展示哪些JAR文件有变化，以及这些JAR中有哪些class文件被修改。这可能需要生成结构化的报告，比如JSON或HTML，方便用户查看。

在实现步骤上，可以分为以下几个部分：

1. 解压主JAR文件：遍历app.jar中的所有条目，识别嵌套的JAR文件（如lib目录下的jar）。

2. 递归解压嵌套JAR：对每个嵌套的JAR，递归执行同样的解压过程，直到所有层级的class文件都被提取出来。

3. 计算哈希值：对每个class文件计算哈希值，记录其相对路径和哈希。

4. 对比两次构建的哈希集合：找出哈希值不同的class文件，进而确定哪些嵌套的JAR发生了变化。

5. 生成差异报告：将对比结果整理成报告，指出有变化的JAR和对应的class文件。

在处理过程中，可能会遇到路径冲突或重复的JAR文件，需要确保路径的唯一性，比如使用嵌套路径作为前缀。同时，需要处理可能存在的相同JAR不同版本的情况，比如依赖升级导致的lib目录下jar的变化。

另外，性能优化方面，可以考虑并行处理嵌套JAR的解压和哈希计算，利用多线程提高处理速度。对于大型项目，可能会有成千上万的class文件，需要确保工具的高效性。

测试方面，需要准备两个不同版本的app.jar，其中一个包含修改过的class文件，另一个未修改，验证工具是否能正确识别出变化。同时，测试嵌套多层JAR的情况，确保递归解压和对比的正确性。

最后，用户可能希望工具能够集成到CI/CD流程中，因此需要考虑命令行接口和输出格式的友好性，比如支持静默模式或机器可读的输出（如JSON），便于自动化处理。

总结来说，这个工具需要具备递归解压、哈希计算、差异对比和报告生成的功能，同时兼顾性能和准确性。需要仔细处理嵌套结构，正确识别class文件的变动，排除无关的二进制差异，确保结果可靠。

以下是一个Java工具的实现方案，用于对比两次Maven构建生成的app.jar中的嵌套JAR和Class文件差异，仅识别实际内容变化的Class文件。该方案基于递归解压、哈希计算和差异标记，支持多层嵌套JAR分析。

工具完整代码

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import java.io.*;
import java.nio.file.*;
import java.security.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class JarDiffTool {

    // 1. 递归解压JAR并收集所有Class文件的哈希
    private static Map<String, String> collectClassHashes(Path jarPath) throws Exception {
        Map<String, String> hashMap = new ConcurrentHashMap<>();
        Deque<Path> jarQueue = new ConcurrentLinkedDeque<>();
        jarQueue.add(jarPath);

        ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());

        while (!jarQueue.isEmpty()) {
            Path currentJar = jarQueue.poll();
            try (ZipInputStream zis = new ZipInputStream(Files.newInputStream(currentJar))) {
                ZipEntry entry;
                while ((entry = zis.getNextEntry()) != null) {
                    Path entryPath = Paths.get(currentJar.getParent().toString(), entry.getName());
                    if (entry.getName().endsWith(".jar")) {
                        // 解压嵌套JAR并加入队列
                        Path nestedJar = extractNestedJar(zis, entryPath);
                        jarQueue.add(nestedJar);
                    } else if (entry.getName().endsWith(".class")) {
                        executor.submit(() -> {
                            try {
                                // 计算Class文件哈希
                                String hash = computeHash(zis);
                                String relativePath = generateRelativePath(currentJar, entry);
                                hashMap.put(relativePath, hash);
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        });
                    }
                }
            }
        }

        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.HOURS);
        return hashMap;
    }

    // 2. 生成相对路径标识（包含嵌套层级）
    private static String generateRelativePath(Path jarPath, ZipEntry entry) {
        String jarName = jarPath.getFileName().toString();
        return jarName + "!/" + entry.getName(); // 例如：app.jar!/lib/dependency.jar!/MyClass.class
    }

    // 3. 计算文件哈希（SHA-256）
    private static String computeHash(InputStream is) throws NoSuchAlgorithmException, IOException {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] buffer = new byte[8192];
        int bytesRead;
        while ((bytesRead = is.read(buffer)) != -1) {
            md.update(buffer, 0, bytesRead);
        }
        return bytesToHex(md.digest());
    }

    // 4. 提取嵌套JAR到临时目录
    private static Path extractNestedJar(ZipInputStream zis, Path targetPath) throws IOException {
        Files.createDirectories(targetPath.getParent());
        try (OutputStream os = Files.newOutputStream(targetPath)) {
            byte[] buffer = new byte[8192];
            int len;
            while ((len = zis.read(buffer)) > 0) {
                os.write(buffer, 0, len);
            }
        }
        return targetPath;
    }

    // 5. 对比两次构建的哈希
    private static ObjectNode compareHashes(Map<String, String> oldHashes, Map<String, String> newHashes) {
        ObjectMapper mapper = new ObjectMapper();
        ObjectNode result = mapper.createObjectNode();
        ArrayNode changedClasses = mapper.createArrayNode();

        // 查找变化的Class
        newHashes.entrySet().stream()
                .filter(e -> !oldHashes.getOrDefault(e.getKey(), "").equals(e.getValue()))
                .forEach(e -> changedClasses.add(e.getKey()));

        // 查找新增/删除的JAR
        Set<String> allJars = new HashSet<>();
        allJars.addAll(oldHashes.keySet().stream().map(k -> k.split("!/")[0]).collect(Collectors.toSet()));
        allJars.addAll(newHashes.keySet().stream().map(k -> k.split("!/")[0]).collect(Collectors.toSet()));

        ArrayNode modifiedJars = mapper.createArrayNode();
        allJars.forEach(jar -> {
            boolean oldExists = oldHashes.keySet().stream().anyMatch(k -> k.startsWith(jar));
            boolean newExists = newHashes.keySet().stream().anyMatch(k -> k.startsWith(jar));
            if (oldExists && !newExists) {
                modifiedJars.add("[DELETED] " + jar);
            } else if (!oldExists && newExists) {
                modifiedJars.add("[ADDED] " + jar);
            } else if (changedClasses.size() > 0) {
                modifiedJars.add("[MODIFIED] " + jar);
            }
        });

        result.set("modified_jars", modifiedJars);
        result.set("changed_classes", changedClasses);
        return result;
    }

    // 工具入口
    public static void main(String[] args) throws Exception {
        Path jar1 = Paths.get("path/to/first/app.jar");
        Path jar2 = Paths.get("path/to/second/app.jar");

        // 收集两次构建的哈希
        Map<String, String> hashes1 = collectClassHashes(jar1);
        Map<String, String> hashes2 = collectClassHashes(jar2);

        // 生成对比报告
        ObjectNode report = compareHashes(hashes1, hashes2);
        System.out.println(new ObjectMapper().writerWithDefaultPrettyPrinter().writeValueAsString(report));
    }

    // 辅助方法：字节转十六进制
    private static String bytesToHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}

工具特性

1. 递归解压嵌套JAR

  • 自动识别lib/*.jar等嵌套依赖

  • 使用多线程加速解压和哈希计算

2. 精准Class差异检测

  • 通过SHA-256哈希算法识别文件内容变化

  • 忽略时间戳、MANIFEST等元数据差异

3. 结构化输出报告

{
  "modified_jars" : [
    "[MODIFIED] app.jar!/lib/commons-lang3-3.12.0.jar",
    "[ADDED] app.jar!/lib/new-dependency.jar"
  ],
  "changed_classes" : [
    "app.jar!/lib/commons-lang3-3.12.0.jar!/org/apache/commons/lang3/StringUtils.class",
    "app.jar!/com/example/MainController.class"
  ]
}

4. 性能优化

  • 线程池处理大规模文件

  • 内存缓存避免重复解压

使用场景示例

1. CI/CD流水线集成
在构建后自动对比当前版本与上一版本的JAR差异，阻止未经验证的变更发布。

2. 依赖冲突排查
快速定位因依赖升级导致的Class文件变化。

3. 安全审计
验证第三方JAR是否被篡改（对比哈希值是否与官方版本一致）。

实现原理

步骤 技术方案
递归解压 使用ZipInputStream逐层解压，维护解压队列
哈希计算 SHA-256算法 + 内存缓存（避免重复计算相同文件）
多线程优化 ExecutorService线程池处理嵌套JAR和Class文件
差异分析 对比两次构建的哈希映射表，识别新增/删除/修改的条目

通过此工具，可以快速识别两次构建中实际发生代码变化的JAR和Class文件，避免因构建环境差异导致的误判。
"""

# 执行文本清洗
cleaned_text = process_text(text)
print("清洗后文本:\n", cleaned_text)
