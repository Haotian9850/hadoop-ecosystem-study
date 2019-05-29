import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import javax.imageio.IIOException;
import java.io.IOException;
import java.util.StringTokenizer;

public class MapperClass extends Mapper<LongWritable, Text, Text, IntWritable> {

    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException{

        String line = value.toString();

        StringTokenizer st = new StringTokenizer(line, "");

        while(st.hasMoreTokens()){
            word.set(st.nextToken());
            context.write(word, one);
        }
    }
}
