package uavnetwork;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;
import java.util.Random;

import javax.vecmath.Point3d;

//llimport static java.lang.Math.sqrt;

import javax.vecmath.Vector3d;

public class UtilityFunctions
{
	private static Properties prop;
	private static int count;
	static
	{
		prop = new Properties();
		count = 1;
		InputStream is;
		try
		{
			is = new FileInputStream("src/main/resources/config.ini");
			prop.load(is);
		} catch (FileNotFoundException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
	
	

	public static int getCount()
	{
		return count;
	}

	public static void setCount(int count)
	{
		UtilityFunctions.count = count;
	}

	public static double interUavDistance(Point3d p1, Point3d p2)
	{
		double distance = p1.distance(p2);
		return distance;
	}

	public static Packet generatePacket(int num)
	{
		Packet p = new Packet();

		Random r = new Random();
		int sender = r.nextInt(num);

		// String[] nbr = prop.getProperty("" + sender).split(",");
		// int index = r.nextInt(nbr.length);
		int receiver = r.nextInt(num);// Integer.parseInt(nbr[index]);

		if (sender == receiver)
		{
			// System.out.println("Sender = "+ sender +"Receiver = "+receiver);
			receiver = (sender + 1) % num;
			// System.out.println("Sender = "+ sender +"Receiver = "+receiver);
		}

		p.setPacketId(count++);
		p.setSenderId(sender);
		p.setRecevierId(receiver);
		

		return p;

	}

	public static Point3d movement(Point3d p1, Point3d p2, double distance, double x_coord, double y_coord)
	{
		// movement of a vector to another by inter-uav distance of 5 m
		double factor;
		factor = distance; // factor by which vector will move

		double uavDistance = interUavDistance(p1, p2);
		Point3d orgPt = new Point3d(x_coord, y_coord, 30);
		while (factor >= uavDistance && factor > 0)
		{
			factor = factor / 2;
		}

		Point3d new_vector = new Point3d();

		if (factor > 0)
		{

			Vector3d diff_vec = new Vector3d(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z);
			Vector3d p1_vec = new Vector3d(p1.x, p1.y, p1.z);

			diff_vec.normalize(); // create unit vector along the direction
			/*
			 * System.out.println(diff_vec.x); System.out.println(diff_vec.y);
			 * System.out.println(diff_vec.z);
			 */
			// new coordinates moved by mentioned factor
			new_vector.x = p1_vec.x + (diff_vec.x) * factor;
			new_vector.y = p1_vec.y + (diff_vec.y) * factor;
			new_vector.z = p1_vec.z + (diff_vec.z) * factor;
			
			double orgDist = interUavDistance(p1, orgPt);
			if(orgDist>=15)
				new_vector = p1;

		}
		return new_vector;
	}

	/*
	 * public static void main(String ar[]) { // Point3d p1 = new Point3d(3.0, 4.0,
	 * 5.0); // Point3d p2 = new Point3d(3.0, 4.0, 7.0);
	 * 
	 * Point3d p1 = new Point3d(1.0, 2.0, 3.0); Point3d p2 = new Point3d(20.0, 30.0,
	 * 45.0);
	 * 
	 * Point3d new_vector; double distance; distance = interUavDistance(p1, p2);
	 * new_vector = movement(p1, p2, distance); //
	 * System.out.println(interUavDistance(p1, p2)); System.out.println(distance);
	 * System.out.println("New x y z coordinates after 20 m movement");
	 * System.out.println(new_vector.x); System.out.println(new_vector.y);
	 * System.out.println(new_vector.z); System.out.println("New distance from p1");
	 * System.out.println(interUavDistance(p1, new_vector));
	 * 
	 * distance = interUavDistance(new_vector, p2); new_vector =
	 * movement(new_vector, p2, distance);
	 * System.out.println("New x y z coordinates after further 20 m movement");
	 * System.out.println(new_vector.x); System.out.println(new_vector.y);
	 * System.out.println(new_vector.z);
	 * System.out.println("New distance from p1 now");
	 * System.out.println(interUavDistance(p1, new_vector));
	 * 
	 * }
	 */
}
