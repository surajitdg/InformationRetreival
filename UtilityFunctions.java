package uavnetwork;

import java.util.Random;

import javax.vecmath.Point3d;

//llimport static java.lang.Math.sqrt;

import javax.vecmath.Vector3d;

public class UtilityFunctions
{
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
		int receiver = r.nextInt(num);
		
		if(sender == receiver)
			{
				//System.out.println("Sender = "+ sender +"Receiver = "+receiver);
				receiver = (sender+1)%num;
				//System.out.println("Sender = "+ sender +"Receiver = "+receiver);
			}
		
		p.setPacketId(r.nextInt());
		p.setSenderId(sender);
		p.setRecevierId(receiver);
			
		
		return p;
		
	}	
		public static Point3d movement (Point3d p1,Point3d p2,double distance)
		{
		// movement of a vector to another by inter-uav distance of 20 m
		double factor;
		factor = 20; //factor by which vector will move
		Point3d new_vector =  new Point3d();
        Vector3d diff_vec = new Vector3d(p2.x-p1.x,p2.y-p1.y,p2.z-p1.z);
        Vector3d p1_vec = new Vector3d(p1.x,p1.y,p1.z);
		
		diff_vec.normalize(); //create unit vector along the direction
		System.out.println(diff_vec.x);
		System.out.println(diff_vec.y);
		System.out.println(diff_vec.z);
        
		
		//new coordinates moved by mentioned factor
		new_vector.x = p1_vec.x+(diff_vec.x)*factor;
		new_vector.y = p1_vec.y+(diff_vec.y)*factor;
		new_vector.z = p1_vec.z+(diff_vec.z)*factor;
		
		
	    
		
	   return new_vector;
			
			
			
		}
	
	
	
	
	public static void main(String ar[])
	{
		//Point3d p1 = new Point3d(3.0, 4.0, 5.0);
		//Point3d p2 = new Point3d(3.0, 4.0, 7.0);
		
		Point3d p1 = new Point3d(1.0, 2.0, 3.0);
		Point3d p2 = new Point3d(20.0, 30.0, 45.0);
		
		Point3d new_vector;
		double distance;
		distance = interUavDistance(p1, p2);
		new_vector = movement(p1,p2,distance);
		//System.out.println(interUavDistance(p1, p2));
		System.out.println(distance);
		System.out.println("New x y z coordinates after 20 m movement");
		System.out.println(new_vector.x);
		System.out.println(new_vector.y);
		System.out.println(new_vector.z);
		System.out.println("New distance from p1");
		System.out.println(interUavDistance(p1,new_vector));
		
		distance = interUavDistance(new_vector, p2);
		new_vector = movement(new_vector,p2,distance);
		System.out.println("New x y z coordinates after further 20 m movement");
		System.out.println(new_vector.x);
		System.out.println(new_vector.y);
		System.out.println(new_vector.z);
		System.out.println("New distance from p1 now");
		System.out.println(interUavDistance(p1,new_vector));
		
	}
}
