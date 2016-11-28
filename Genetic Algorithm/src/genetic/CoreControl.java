package genetic;
/** 
 * @author 崔平
 * @date 2016/11/27
 */
import java.util.Random;

public class CoreControl {     // 核心控制类
	
	/**
	 * 主要参数
	 * @param A                区间下界
	 * @param B                区间上界
	 * @param interalX1        X1 区间 
	 * @param interalX2        X2 区间 
	 * @param problemThings[]  问题相关的 数字
	 * @param members[]        种群的成员
	 * @param LENGTH           编码长度
	 * @param stop             停止的代数
	 * @return  
	 */
	
	public static final double X1_A=-3;//区间下界
	public static final double X1_B=12.1;//区间上界
	public static final double interalX1 = X1_B-X1_A;//区间
	public static final double X2_A=4.1;//区间下界
	public static final double X2_B=5.8;//区间上界
	public static final double interalX2 = X2_B-X2_A;//区间
	public double[] problemThings = new double[SpeciesGroup.size];//问题相关的 数字
	public String[] members = new String[SpeciesGroup.size];
	
	public static final int LENGTH=33;//编码长度，因为要精确到小数点后六位，所以编为LENGTH位长，有一公式可参考
	
	public static final int stop = 100;//停止的代数
	
	
	/**
	 * 编码
	 */
	public void encode(){
		int size_index = 0; 
		while(size_index < SpeciesGroup.size){
			Random rand = new Random();
			int[] int_gen = new int[LENGTH];//十进制形式 成员的
			for(int i = 0;i < LENGTH;i++){
				int_gen[i] = rand.nextInt(2);//随机生成一个只包含0/1的33位的数组
//				System.out.print(int_gen[i]);
			}
//			System.out.println();
			String sb = new String("");
			for(int i = 0; i < LENGTH; i++){
				sb += Integer.toString(int_gen[i]);
			}
			members[size_index] = sb;
			size_index += 1;
		}
	}
	
	/**
	 * 判断是否结束
	 */
	boolean isEnded(){
		if(SpeciesGroup.generation < stop)
			return false;
		else
			return true;
	}
	
	/**
	 * 初始化
	 * @param args
	 */
	Random randomNumber=new Random();
	public void initialize(){
		encode();
	}
	
	public String[] getMembers(){
		return members;
	}
	public static void main(String[] args) {
		CoreControl a = new CoreControl();
		a.initialize();
		for (int i = 0; i < a.members.length; i++) {
			System.out.println(a.members[i]);
		}
	}
}
