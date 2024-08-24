using ClassLibrary1.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Text.Json;

namespace PythonApiExample.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class PythonController : ControllerBase
    {
        private readonly ILogger<PythonController> _logger;

        public PythonController(ILogger<PythonController> logger)
        {
            _logger = logger;
        }

        // POST: /Python
        [HttpPost("GenerateSingleImage")]
        public IActionResult RunPythonScript([FromBody] PythonRequest request)
        {
            string pythonScriptPath = "c:\\Users\\2309013\\Desktop\\後端製圖\\pythonGenerateImage-main\\Test.py";
            string outputDirectory = "c:\\Users\\2309013\\Desktop\\後端製圖\\pythonGenerateImage-main\\output_images";
            string tempJsonFilePath = Path.Combine(Path.GetTempPath(), $"{Guid.NewGuid()}.json");

            var options = new JsonSerializerOptions
            {
                Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
                WriteIndented = true
            };

            // 將所有的圖像請求序列化為一個 JSON
            string jsonData = JsonSerializer.Serialize(request.Images, options);
            System.IO.File.WriteAllText(tempJsonFilePath, jsonData);

            _logger.LogInformation("Serialized JSON Data: {jsonData}", jsonData);

            // 執行 Python 腳本
            var start = new ProcessStartInfo
            {
                FileName = "python",
                Arguments = $"\"{pythonScriptPath}\" \"{tempJsonFilePath}\"",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using (var process = Process.Start(start))
            {
                string result = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();

                if (!string.IsNullOrEmpty(error))
                {
                    System.IO.File.Delete(tempJsonFilePath);
                    return BadRequest(new { message = "Python script error", error });
                }
            }

            System.IO.File.Delete(tempJsonFilePath);

            // 假設只會生成單張圖片
            string outputImagePath = Path.Combine(outputDirectory, $"colored_map_{request.Images.Keys.First()}.png");
            if (!System.IO.File.Exists(outputImagePath))
            {
                return NotFound(new { message = "Image not found", key = request.Images.Keys.First() });
            }

            byte[] fileBytes = System.IO.File.ReadAllBytes(outputImagePath);
            return File(fileBytes, "image/png");
        }


        [HttpPost("GenerateMultipleImages")]
        public IActionResult GenerateMultipleImages([FromBody] PythonRequest request)
        {
            string pythonScriptPath = "c:\\Users\\2309013\\Desktop\\後端製圖\\pythonGenerateImage-main\\Test.py";
            string outputDirectory = "c:\\Users\\2309013\\Desktop\\後端製圖\\pythonGenerateImage-main\\output_images";
            string zipFilePath = "c:\\Users\\2309013\\Desktop\\後端製圖\\pythonGenerateImage-main\\output_images.zip";
            string tempJsonFilePath = Path.Combine(Path.GetTempPath(), $"{Guid.NewGuid()}.json");

            var options = new JsonSerializerOptions
            {
                Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
                WriteIndented = true
            };

            try
            {
                // 將所有請求資料一次性序列化為一個JSON文件
                string jsonData = JsonSerializer.Serialize(request.Images, options);
                System.IO.File.WriteAllText(tempJsonFilePath, jsonData);

                _logger.LogInformation("Serialized JSON Data: {jsonData}", jsonData);

                // 準備執行 Python 腳本
                var start = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = $"\"{pythonScriptPath}\" \"{tempJsonFilePath}\"",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using (var process = Process.Start(start))
                {
                    string result = process.StandardOutput.ReadToEnd();
                    string error = process.StandardError.ReadToEnd();

                    if (!string.IsNullOrEmpty(error))
                    {
                        System.IO.File.Delete(tempJsonFilePath);
                        return BadRequest(new { message = "Python script error", error });
                    }
                }

                System.IO.File.Delete(tempJsonFilePath);

                // 壓縮 outputDirectory 資料夾
                if (System.IO.File.Exists(zipFilePath))
                {
                    System.IO.File.Delete(zipFilePath);
                }
                ZipFile.CreateFromDirectory(outputDirectory, zipFilePath);

                // 返回ZIP文件
                byte[] fileBytes = System.IO.File.ReadAllBytes(zipFilePath);
                return File(fileBytes, "application/zip", "output_images.zip");
            }
            catch (Exception ex)
            {
                _logger.LogError("An error occurred: {ex}", ex);
                return StatusCode(500, new { message = "Internal server error", detail = ex.Message });
            }
            finally
            {
                // 確保臨時文件被刪除
                if (System.IO.File.Exists(tempJsonFilePath))
                {
                    System.IO.File.Delete(tempJsonFilePath);
                }
            }
        }




    }
}
