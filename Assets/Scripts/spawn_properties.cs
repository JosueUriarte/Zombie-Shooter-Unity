using System.Collections;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using UnityEngine;

public class spawn_properties : MonoBehaviour
{

    public GameObject regular_zombie;
    public GameObject fast_zombie;
    public GameObject buff_zombie;

    public float percent_fast_zombie;
    public float percent_buff_zombie;

    public float spawnTime;
    public float spawnDelay;
    public float spawner_health = 15f;

    // Start is called before the first frame update
    void Start()
    {
    	InvokeRepeating("Spawner", spawnTime, spawnDelay);
    }

    /**
    void OnCollisionEnter(Collision collision)
    {
        if(collision.gameObject.tag == "Bullet"){
            Debug.Log("collision detected!");
            Destroy(this.gameObject);
        }
    }
    **/

    void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.tag == "Bullet")
        {
			spawner_health -= 1;
        }
    }

    void Update()
	{
		if (spawner_health <= 0)
		{
			Destroy(gameObject);
		}
	}

    void Spawner()
	{
		Instantiate(regular_zombie, transform.position, transform.rotation);

		if(Random.value <= percent_fast_zombie) //%20 percent chance
        {
            Instantiate(fast_zombie, transform.position, transform.rotation);
        }

        if(Random.value <= percent_buff_zombie) //%10 percent chance
        {
            Instantiate(buff_zombie, transform.position, transform.rotation);
        }
	}
}
