package genetic;
/** 
 * @author 崔平
 * @date 2016/11/27
 */

import java.util.Random;


public class SpeciesGroup {
	
	/**
	 * @param size             种群大小 
	 * @param member[]         种群成员
	 * @param fitness[]        成员适应度
	 * @param generation       代数
	 * @param VProbability     变异属性
	 * @param IProbability     交叉属性
	 * @param lengthOfCode     染色体基因个数  || 码长
	 * @param problemThings[]  问题相关的 数字
	 * @param bestOneEnode      最优个体编码
	 * @param bestOneFit       最优个体适应度
	 * @param bestOneNum       最优个体适应度
	 * @return  
	 */
	
	
	/**
	 * 主属性	
	 */
	static int size = 100;//种群大小；
	String bestOneEncode ="";
	double bestOneFit = 0;
	double bestOneNum[] = new double[2];
	String[] member = new  String[SpeciesGroup.size];//种群成员；
	double[] fitness = new  double[SpeciesGroup.size];//成员适应度
	
	static int generation = 0;//代数
	double VProbability = 0.1;//变异概率
	double IProbability = 0.9;//交叉概率
	static int lengthOfCode = 33;//染色体基因个数  || 码长
	static int lengthOfX_1 = 18;//X1染色体基因个数  || 码长
	static int lengthOfX_2 = 15;//X2染色体基因个数  || 码长
	static int MJX_1 = (int) Math.pow(2, 18)-1;//2^X1
	static int MJX_2 = (int) Math.pow(2,15)-1;//2^X2
	/**
	 * 工具属性	
	 */
	Random randomNumber=new Random();
	public double[][] problemThings = new double[SpeciesGroup.size][2];//问题相关的 数字
	
	/**
	 * 方法实现
	 * @param firstGeneration
	 */
	SpeciesGroup(String[] firstGeneration){
		for(int i = 0;i<size;i++){
			member[i] = firstGeneration[i];
		}
//		for (int i = 0; i < member.length; i++) {
//			System.out.println(member[i]);
//		}
		//进行解码
		decode();
	}
	

	public void encode(){
		int size_index = 0; 
		while(size_index < SpeciesGroup.size){
			Random rand = new Random();
			int[] int_gen = new int[lengthOfCode];//十进制形式 成员的
			for(int i = 0;i < lengthOfCode;i++){
				int_gen[i] = rand.nextInt(2);//随机生成一个只包含0/1的33位的数组
			}

			String sb = new String();
			for(int i=1;i<int_gen.length;i++){
				sb += Integer.toString(int_gen[i]);
			}
			member[size_index] = sb;
			size_index += 1;
		}
	}
	
	/**
	 * 第一个输出平均适应度，第二个输出最大适应度
	 * @return
	 */
	public double[] getValues(){
		double[] values = new double[2] ;
		
		double sum = 0 ;
		for(int i = 0 ; i < fitness.length ; i ++){
			sum += fitness[i] ;
		}
		
		values[0] = sum / fitness.length ;
		values[1] = bestOneFit ;
		
		return values ;
	}
	
	
	/**
	 * 解码
	 */
	public void decode(){
		int k=0,m=0;//十进制形式 成员的
		int mum_index = 0;
		
		while (mum_index < SpeciesGroup.size) {
			String sub_X1 = member[mum_index].substring(0, lengthOfX_1);
			k = Integer.parseInt(sub_X1, 2);
			problemThings[mum_index][0] = CoreControl.X1_A + CoreControl.interalX1/MJX_1*k;
			
			String sub_X2 = member[mum_index].substring(lengthOfX_1, lengthOfCode);
			m = Integer.parseInt(sub_X2, 2);
			problemThings[mum_index][1] = CoreControl.X2_A + CoreControl.interalX2/MJX_2*m;
			m = 0;
			k = 0;
			mum_index += 1;
		}
		
	}
	
	/**
	 * 变异 
	 */
	public void variation(){
		for(int i=0;i<size;i++){
			if(randomNumber.nextDouble()<=VProbability){

				int changePlace=randomNumber.nextInt(lengthOfCode);  //随机选择一位取反
				StringBuffer sb=new StringBuffer(member[i]);
				
				if(sb.charAt(changePlace)=='0'){     
					sb.setCharAt(changePlace, '1');			//取反	 						
				}
				else if(sb.charAt(changePlace)=='1'){		
					sb.setCharAt(changePlace, '0');         //取反
				}
				else{
					System.out.println("出错！！！");
				}
				member[i]=sb.toString();

			}
			else{				
			}
		}
	}
	
	/**
	 * 交叉
	 */
	public void intersect(){
		for(int i = 0;i <= size/2;i++){
			if(Math.random() <= IProbability){
				int one = randomNumber.nextInt(size);//随机选出 一个 个体
				int theOther = randomNumber.nextInt(size);//随机选出另一个个体
				int intersection = randomNumber.nextInt(lengthOfCode);//随机产生 交叉点
							
				String str_one = member[one].substring(intersection);
				String str_theOther = member[theOther].substring(intersection);

				
				StringBuffer sb = new StringBuffer(member[one]);//交换第一个 个体
				sb.replace(intersection, lengthOfCode,str_theOther);
				member[one] = sb.toString();
				
			    sb = new StringBuffer(member[theOther]);//交换第二个 个体
				sb.replace(intersection, lengthOfCode,str_one);
				member[theOther] = sb.toString();
				
 			}
			else{				
			}
		}
	}
	
	/**
	 * 轮盘赌方法
	 */
	public void gambleWheel_1()
	{ 
	   double sum=0;
	   for (int i = 0; i <size; i++) {
		   sum=fitness[i]+sum;
	   }

	   double[] p = new double[SpeciesGroup.size]; //适应度的概率
	   for (int i = 0; i < size; i++) {
		   p[i]=fitness[i]/sum;
	   }
	   double[] q = new double[SpeciesGroup.size];
	   for (int i = 0; i < size; i++) {
		   for (int j = 0; j < i+1; j++) {	     
			  q[i]+=p[j];
	       }
	   }
	   double[] ran=new double[50];
	   String[] tempPop=new String[50];
	   for (int i = 0; i < ran.length; i++) {	    
		   ran[i]=randomNumber.nextDouble();
	   }
	   for (int i = 0; i < ran.length; i++) {	    
		   int k = 0;	  
		   for (int j = 0; j < q.length; j++) {	    
			   if(ran[i]<q[j]){	     
				   k=j;	      
				   break;	    
			   }	     
			   else continue;	    
		   }	    
		   tempPop[i]=member[k];	  
	   }
	   for (int i = 0; i < tempPop.length; i++) {	    
		   member[i]=tempPop[i];
	   }
	}
	
	/**
	 * 赌轮选择 
	 */
	public void gambleWheel(){	
		double sum=0;//适应度之和
		for(int i=0;i<SpeciesGroup.size;i++){
			sum+=fitness[i];
		}
		
		double[] fProbability = new double[SpeciesGroup.size]; //适应度的概率
		for(int i=0;i<SpeciesGroup.size;i++){
			fProbability[i] = fitness[i]/sum;
		}

		double[] wheelBorder = new double[SpeciesGroup.size+1];//赌轮 边界
		wheelBorder[0] = 0;
		for(int i = 0;i<SpeciesGroup.size;i++){
			for(int j = 0;j<=i;j++){
				wheelBorder[i+1] +=   fProbability[j];
			}
		}
		
		double pointer = 0;
		String[]tempMember = new  String[SpeciesGroup.size];//下一代 临时种群成员；
		for(int i = 0;i<SpeciesGroup.size;i++){
		// pointer = Math.random();                     //  模仿赌轮指针  			
			pointer = randomNumber.nextDouble();			 
			for(int j=0;j<wheelBorder.length-1;j++){		//赌轮 转动 后 指针 随机 指向 赌轮 中的一块区域				 
				if(pointer>=wheelBorder[j]&&pointer<wheelBorder[j+1]){//确定是那块区域					 
					tempMember[i] = member[j];           //     结果临时保存  以免影响 种群属性					 
					break;				 
				}				 
				else {				 
				}			 			
			}		
		}
		for(int i = 0;i<SpeciesGroup.size;i++){//临时 成员  转化 为 真实 成员			
			member[i] = tempMember[i];
		}	
	}
	
	/**
	 * 返回最大的适应度值
	 * f==x1sin(4*pi*x1)+x2sin(13*pi*x2)+18
	 */
	public double sufficiency(){
	//	String theBest=null;
		int max = 0;
		int min = 0;
		for(int i = 0;i<SpeciesGroup.size;i++){
			fitness[i] = problemThings[i][0]*Math.sin(Math.PI*4*problemThings[i][0]) +
					problemThings[i][1]*Math.sin(Math.PI*13*problemThings[i][1])+18;
			if(fitness[max]<fitness[i]){
				max = i;
			}
			if(fitness[min]>fitness[i]){
				max = i;
			}
		}
		if (fitness[max] >= bestOneFit) {
			bestOneFit = fitness[max];
			bestOneEncode = member[max];
			bestOneNum = problemThings[max];
			System.out.println("x1=："+problemThings[max][0]);        //输出每次迭代适应度最大对应的x值
			System.out.println("x2=："+problemThings[max][1]);        //输出每次迭代适应度最大对应的x值
			System.out.println("Encode=：" + member[max]);
			return fitness[max];
		}else{
			fitness[min] = bestOneFit;
			member[min] = bestOneEncode;
			problemThings[min] = bestOneNum;
			System.out.println("x1=："+problemThings[min][0]);        //输出每次迭代适应度最大对应的x值
			System.out.println("x2=："+problemThings[min][1]);        //输出每次迭代适应度最大对应的x值
			System.out.println("Encode=：" + member[min]);
			return fitness[min];
		}
		

	}
	
	
	
	/**
	 * 下一代
	 */
	public void nextGeneration(){	
		//gambleWheel_1();  //选择
		gambleWheel();      //选择		
		
		intersect();   		//交叉
		variation();   		//变异
		SpeciesGroup.generation++;         //不停迭代到下一代
	}
	
	/**
	 * 输出种群成员
	 */
	public void print(){
		for(int i=0;i< SpeciesGroup.size;i++){
			System.out.println(member[i]);
		}
	}
	
	/**
	 * 主函数
	 * @param args
	 */
	public static void main(String[] args) {
		CoreControl control = new CoreControl();
		control.initialize();        //进行初始化

		SpeciesGroup speciesGroup = new SpeciesGroup(control.getMembers());
    }

}
