<?php
header('Content-Type: application/json; charset=utf-8');
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);

    $model = (empty($data['model']) ||  $data['model'] == 'custom') 
            ? "dev/runs/detect/train8/weights/best" 
            : $data['model'];
    $gpu = $data['gpu'] ?? false;
    $confidence_threshold = $data['confidence'] ?? 0.60;

    
    try {
        // Modificar YAML
        // Leer el archivo YAML
        $yamlContent = yaml_parse_file('./config.yaml');
        
        // Modificar los valores que necesites
        $yamlContent['model_path'] = "$model.pt";
        // $yamlContent['camera_index'] = 1;
        $yamlContent['gpu'] = $gpu;
        $yamlContent['confidence_threshold'] = $confidence_threshold;
        
        // Modificar o agregar clases
        // $yamlContent['class_names'][0] = "una manzana";
        // $yamlContent['class_names'][52] = "una pera";
        
        // Guardar los cambios
        $newYamlContent = yaml_emit($yamlContent);
        file_put_contents('./new_config.yaml', $newYamlContent);

        $response = [
            "status" => "success",
            'ok' => true,
            "code" => 200,
            "message" => "Configuration was updated successfully.",
            "data"=> $data,
            'timestamp' => date('c'), // Marca de tiempo en formato ISO 8601
            "errors" => null
        ];
    } catch (\Throwable $th) {
        //throw $th;
        // echo $th;
        $response = [
            'status' => 'error',
            'ok' => false,
            'code' => 400,
            'message' => "There was an issue while trying to update config file.",
            'data' => null,
            'errors' => [
                'Data was received, but there is an unknow error'
                ]
            ];
        }
        // echo "Archivo YAML actualizado con éxito.";       
}

echo json_encode($response);
?>