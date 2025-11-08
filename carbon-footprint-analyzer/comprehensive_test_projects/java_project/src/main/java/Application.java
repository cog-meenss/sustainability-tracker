
public class Application {
    
    public static void main(String[] args) {
        DataProcessor processor = new DataProcessor();
        processor.processData();
    }
    
    static class DataProcessor {
        
        public void processData() {
            // Inefficient nested loops
            for (int i = 0; i < 100; i++) {
                for (int j = 0; j < 100; j++) {
                    String result = "data_" + i + "_" + j;
                    System.out.println(result.length());
                }
            }
        }
    }
}
