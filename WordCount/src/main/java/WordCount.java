import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class WordCount extends Configured implements Tool{

    public int run(String[] args) throws Exception{
        if(args.length != 2){
            System.out.println("Incorrect number of arguments");
            return -1;
        }

        Job job = new Job();
        job.setJarByClass(WordCount.class);
        job.setJobName("WordCounter");

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        job.setOutputFormatClass(TextOutputFormat.class);

        job.setMapperClass(MapperClass.class);
        job.setReducerClass(ReducerClass.class);

        int returnValue = job.waitForCompletion(true) ? 0 : 1;

        if(job.isSuccessful()){
            System.out.println("Success!");
        }else{
            System.out.println("FAIL!!!");
        }

        return returnValue;

    }

    public static void main(String[] args) throws Exception{
        int exitCode = ToolRunner.run(new WordCount(), args);
        System.exit(exitCode);
    }
}
